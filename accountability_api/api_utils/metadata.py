COMPOSITE_RELEASE_ID_FIELD = "CompositeReleaseID"

PRODUCTS_INDEX = "*"

LAST_MODIFIED_FIELD = "LastModifiedTime"

PRODUCT_COUNTER = "ProductCounter"

TIMER_INDEX = "timer_status"

# TODO chrisjrd: finalize. Placing entries here because Bach UI uses it in the Data Summary > Incoming screen.
ANCILLARY_INDEXES = {
    "HLS_L30": "grq_1_l2_hls_l30",
    "HLS_S30": "grq_1_l2_hls_s30"
}

# TODO chrisjrd: finalize. Currently, the opera_state_config index does not behave like normal *-state-config indexes
#  and so cannot be added to this map.
STATE_CONFIG_INDEXES = {
    "L30_STATE_CONFIG": "grq_1_l2_hls_l30-state-config",
    "S30_STATE_CONFIG": "grq_1_l2_hls_s30-state-config"
}

PRODUCT_INDEXES = {
    "DSWX_HLS": "grq_1_l3_dswx_hls"
}
"""Map of product types to their Elasticsearch indexes."""

ACCOUNTABILITY_INDEXES = {
    "DOWNLINK": "pass_accountability_catalog",
    "OBSERVATION": "observation_accountability_catalog",
    "TRACK_FRAME": "track_frame_accountability_catalog"
}

INCOMING_SDP_PRODUCTS = {
    "HLS_L30": "grq_1_l2_hls_l30",
    "HLS_S30": "grq_1_l2_hls_s30"
}

# TODO chrisjrd: finalize. adding here so the ancillary tab isn't empty (we don't have test data yet)
INCOMING_ANCILLARY_FILES = {
    "HLS_L30": "grq_1_l2_hls_l30",
    "HLS_S30": "grq_1_l2_hls_s30"
}

GENERATED_PRODUCTS = {
    "DSWX_HLS": "grq_1_l3_dswx_hls"
}

OUTGOING_PRODUCTS_TO_DAAC = {
    "DSWX_HLS": "grq_1_l3_dswx_hls"
}

RSLC_CHILDREN = []

MOZART_INDEXES = {"JOB_STATUS": "job_status-current", "TIMER": "timer_status"}
