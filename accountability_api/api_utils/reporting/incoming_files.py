from .report import Report
from accountability_api.api_utils import utils, query, processing
from accountability_api.api_utils import metadata as consts


class IncomingFiles(Report):
    """
    https://docs.google.com/presentation/d/1Qpk2sEkltm2rJJI-GvKiSChl2ljVQ7LDFbWURviFc7I/edit?usp=sharing

    """

    def __init__(
        self, title, start_date, end_date, timestamp, report_type="nen", **kwargs
    ):
        super(IncomingFiles, self).__init__(
            title, start_date, end_date, timestamp, **kwargs
        )
        self._report_type = report_type
        self._total_incoming_data_file_num = 0
        self._total_incoming_data_file_volume = 0
        self._total_products_produced_num = 0
        self._total_products_produced_size = 0

        self._products = {}

    def populate_data(self):
        products = {}
        products = self._get_incoming_products()

        self._products = products

    def _get_incoming_products(self):

        indexes = {}

        if self._report_type == "nen":
            indexes = consts.INCOMING_NEN_PRODUCTS
        elif self._report_type == "gds_ancillary":
            indexes = consts.INCOMING_GDS_ANCILLARY_FILES

        # Go through each index in the incoming_nen_products indexes
        products = []

        total_products_produced = 0
        total_volume = 0

        for index in indexes:
            product_creation = query.construct_range_object(
                "creation_timestamp",
                start_value=self._start_datetime,
                stop_value=self._end_datetime,
            )
            source_includes = [
                "metadata.FileSize",
                "metadata.ProcessingType",
            ]

            body = {
                "query": {"bool": {"must": [{"range": product_creation}]}},
                "_source": source_includes,
            }
            body = self.add_universal_query_params(body)

            try:
                results = query.run_query(
                    index=indexes[index], body=body, doc_type="_doc"
                )

                volume = processing._get_processed_volume(
                    results.get("hits", {}).get("hits", [])
                )
                num_products = len(results.get("hits", {}).get("hits", []))

                total_products_produced += num_products
                total_volume += volume

                products.append(
                    {"name": index, "num_ingested": num_products, "volume": volume}
                )
            except Exception:
                print("could not find index")
                products.append({"name": index, "num_ingested": 0, "volume": 0})

        self._total_incoming_data_file_num = total_products_produced
        self._total_incoming_data_file_volume = total_volume

        return products

    def get_dict_format(self):
        root_name = ""
        if self._report_type == "nen":
            root_name = "INCOMING_NEN_PRODUCTS_REPORT"
        elif self._report_type == "gds_ancillary":
            root_name = "INCOMING_GDS_PRODUCTS_REPORT"

        return {
            "root_name": root_name,
            "header": {
                "time_of_report": self._creation_time,
                "data_recieved_time_range": "{}-{}".format(
                    utils.split_extra_except_t(self._start_datetime),
                    utils.split_extra_except_t(self._end_datetime),
                ),
                "crid": self._crid,
                "venue": self._venue,
                "processing_mode": self._processing_mode,
                "total_products_produced": self._total_incoming_data_file_num,
                "total_data_volume": self._total_incoming_data_file_volume,
            },
            "products": self._products,
        }

    def get_data(self):
        return self._products

    def to_xml(self):
        data = self.get_dict_format()
        root_name = "root"
        if "root_name" in data:
            root_name = data["root_name"]
            del data["root_name"]

        return utils.convert_to_xml_str(root_name, data)

    def to_json(self):
        return super().to_json()

    def to_csv(self):
        return super().to_csv()

    def get_filename(self, output_format):
        return "incoming_{}_files_{}_{}.{}".format(
            self._report_type, self._start_datetime, self._end_datetime, output_format
        )

    def generate_report(self, output_format=None):
        return super().generate_report(output_format=output_format)