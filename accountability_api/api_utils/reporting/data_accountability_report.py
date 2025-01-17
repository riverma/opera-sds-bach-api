import json
from json2xml import json2xml
from json2xml.utils import readfromstring

from .report import Report
from .daac_outgoing_products import DaacOutgoingProducts
from .generated_sds_products import GeneratedSdsProducts
from .incoming_files import IncomingFiles

from accountability_api.api_utils import utils


class DataAccountabilityReport(Report):
    """
    https://docs.google.com/presentation/d/1Qpk2sEkltm2rJJI-GvKiSChl2ljVQ7LDFbWURviFc7I/edit?usp=sharing

    """

    def __init__(
        self, title, start_date, end_date, timestamp, detailed=False, **kwargs
    ):
        super(DataAccountabilityReport, self).__init__(
            title, start_date, end_date, timestamp, detailed=detailed, **kwargs
        )
        self._detailed = detailed
        self._total_incoming_data_file_num = 0
        self._total_incoming_data_file_volume = 0
        self._total_products_produced_num = 0
        self._total_products_produced_volume = 0

        self._reports = {}

    def populate_data(self):
        # DOP = DaacOutgoingProducts GSP = GeneratedSdsProducts IFN = IncomingFilesNen IFG = IncomingFilesGDS
        DOP_report = DaacOutgoingProducts(
            self._title,
            self._start_datetime,
            self._end_datetime,
            self._creation_time,
            detailed=self._detailed,
        )
        GSP_report = GeneratedSdsProducts(
            self._title,
            self._start_datetime,
            self._end_datetime,
            self._creation_time,
            detailed=self._detailed,
        )
        IFN_report = IncomingFiles(
            self._title,
            self._start_datetime,
            self._end_datetime,
            self._creation_time,
            report_type="nen",
        )
        IFG_report = IncomingFiles(
            self._title,
            self._start_datetime,
            self._end_datetime,
            self._creation_time,
            report_type="gds_ancillary",
        )

        reports = {}

        reports["daac_outgoing_products"] = DOP_report._get_daac_outgoing_products()
        reports["generated_sds_products"] = GSP_report._get_generated_products()
        reports["incoming_nen_products"] = IFN_report._get_incoming_products()
        reports["incoming_gds_products"] = IFG_report._get_incoming_products()

        self._total_incoming_data_file_num += (
            IFN_report._total_incoming_data_file_num
            + IFN_report._total_incoming_data_file_num
        )
        self._total_incoming_data_file_volume += (
            IFN_report._total_incoming_data_file_volume
            + IFN_report._total_incoming_data_file_volume
        )
        self._total_products_produced_num += GSP_report._total_products_produced_num
        self._total_products_produced_volume += GSP_report._total_products_volume

        self._reports = reports

    def get_dict_format(self):
        root_name = "DATA_ACCOUNTABILITY_REPORT"

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
                "total_incoming_data_files": self._total_incoming_data_file_num,
                "total_incoming_data_volume": self._total_incoming_data_file_volume,
                "total_products_produced_files": self._total_products_produced_num,
                "total_products_produced_volume": self._total_products_produced_volume,
            },
            "daac_outgoing_products": self._reports["daac_outgoing_products"],
            "generated_sds_products": self._reports["generated_sds_products"],
            "incoming_nen_products": self._reports["incoming_nen_products"],
            "incoming_gds_products": self._reports["incoming_gds_products"],
        }

    def get_data(self):
        return self._reports

    def to_xml(self):
        data = self.get_dict_format()
        if "root_name" in data:
            del data["root_name"]

        xml_data = readfromstring(json.dumps(data))
        result = json2xml.Json2xml(
            xml_data, wrapper="DATA_ACCOUNTABILITY_REPORT", pretty=True, attr_type=False
        ).to_xml()

        return result

    def to_json(self):
        return super().to_json()

    def to_csv(self):
        return super().to_csv()

    def get_filename(self, output_format):
        return "dar_{}_{}_{}_{}.{}".format(
            self._report_type,
            self._creation_time,
            utils.split_extra_except_t(self._start_datetime),
            utils.split_extra_except_t(self._end_datetime),
            output_format,
        )

    def generate_report(self, output_format=None):
        return super().generate_report(output_format=output_format)
