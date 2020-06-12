from yeahml.config.default.types.base_types import (
    categorical,
    list_of_categorical,
    numeric,
)
from yeahml.config.default.types.compound.data import data_set_name_dict
from yeahml.config.default.types.compound.directive import instruct_parser
from yeahml.config.default.types.compound.layer import layers_parser
from yeahml.config.default.types.compound.optimizer import optimizers_parser
from yeahml.config.default.types.compound.performance import performances_parser
from yeahml.config.default.types.param_types import optional_config

# meta
# TODO: set accepted options for `trace_level`
# TODO: ensure `default_load_params_path` is a path.. also, does this belong in
# meta?
# TODO: I'm not sure trace_level is used anymore
# TODO: numbers could probably be converted to string (for experiment_name?)
meta = {
    "meta": {
        # directory
        "yeahml_dir": categorical(
            default_value="yeahml", required=False, is_type=str, to_lower=False
        ),  # could add a check that the location exists
        "data_name": categorical(
            default_value=None, required=True, is_type=str, to_lower=False
        ),
        "experiment_name": categorical(
            default_value=None, required=True, is_type=str, to_lower=False
        ),
        "start_fresh": categorical(default_value=False, required=False, is_type=bool),
        # random seed
        "rand_seed": numeric(default_value=None, required=False, is_type=int),
        # tracing
        "trace_level": categorical(default_value=None, required=False),
        # default path to load param information
        # TODO: this should likely move to the model config
        "default_load_params_path": categorical(
            default_value=None, required=False, is_type=str, to_lower=False
        ),  # TODO: confirm path exists
    }
}


# TODO: some of these values are positive only .. may consider additional check
hyper_parameters = {
    "hyper_parameters": {
        "dataset": {
            "batch": numeric(default_value=None, required=True, is_type=int),
            "shuffle_buffer": numeric(default_value=None, required=False, is_type=int),
        },
        "epochs": numeric(default_value=None, required=True, is_type=int),
        # TODO: need to account for optional outter keys
        "early_stopping": optional_config(
            conf_dict={
                "epochs": numeric(default_value=None, required=False, is_type=int),
                "warm_up": numeric(default_value=None, required=False, is_type=int),
            }
        ),
    }
}

optimize = {
    "optimize": {"optimizers": optimizers_parser(), "directive": instruct_parser()}
}


ERR_LEVELS = [x.lower() for x in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]]

# TODO: it should be acceptable to pass a "CRITICAL" here
logging = {
    "logging": {
        "console": optional_config(
            conf_dict={
                "level": categorical(
                    default_value="critical",
                    required=False,
                    is_in_list=ERR_LEVELS,
                    is_type=str,
                ),
                "format_str": categorical(
                    default_value="%(name)-12s: %(levelname)-8s %(message)s",
                    required=False,
                    is_type=str,
                    to_lower=False,
                ),
            }
        ),
        "file": optional_config(
            conf_dict={
                "level": categorical(
                    default_value="critical",
                    required=False,
                    is_in_list=ERR_LEVELS,
                    is_type=str,
                ),
                "format_str": categorical(
                    default_value="%(filename)s:%(lineno)s - %(funcName)20s()][%(levelname)-8s]: %(message)s",
                    required=False,
                    is_type=str,
                    to_lower=False,
                ),
            }
        ),
        "track": optional_config(
            conf_dict={
                "tracker_steps": numeric(default_value=0, required=False, is_type=int),
                "tensorboard": optional_config(
                    conf_dict={
                        "param_steps": numeric(
                            default_value=0, required=False, is_type=int
                        )
                    }
                ),
            }
        ),
    }
}


# Data
data = {"data": {"datasets": data_set_name_dict(required=True)}}

# NOTE: these two are really simliar, but I think it may be worth keeping them
# separate.. that is I like the idea of being able to define these as separate processes
preprocess = {"preprocess": {}}
augment = {"augment": {}}

# TODO: these need to be moved to preprocess
# # copy is used to prevent overwriting underlying data
# formatted_dict["input_layer_dim"] = None
# formatted_dict["in_dim"] = raw_config["in"]["dim"].copy()
# if formatted_dict["in_dim"][0]:  # as oppposed to [None, x, y, z]
#     formatted_dict["in_dim"].insert(0, None)  # add batching
# formatted_dict["in_dtype"] = raw_config["in"]["dtype"]
# try:
#     formatted_dict["reshape_in_to"] = raw_config["in"]["reshape_to"]
#     if formatted_dict["reshape_in_to"][0] != -1:  # as oppposed to [None, x, y, z]
#         formatted_dict["reshape_in_to"].insert(0, -1)  # -1
# except KeyError:
#     # None in this case is representative of not reshaping
#     formatted_dict["reshape_in_to"] = None
# if formatted_dict["reshape_in_to"]:
#     formatted_dict["input_layer_dim"] = raw_config["in"]["reshape_to"]
# else:
#     formatted_dict["input_layer_dim"] = raw_config["in"]["dim"].copy()
# formatted_dict["augmentation"] = raw_config["image"]["augmentation"]
# formatted_dict["image_standardize"] = raw_config["image"]["standardize"]

# NOTE: this doesn't matter.. unless we're doing supervised. but even still,
# this could be specified/figured out by the var that is passed to the loss/metrics
# formatted_dict["output_dim"] = raw_config["label"]["dim"].copy()
# if formatted_dict["output_dim"][0]:  # as oppposed to [None, x, y, z]
#     formatted_dict["output_dim"].insert(0, None)  # add batching
# formatted_dict["label_dtype"] = raw_config["label"]["dtype"]
# formatted_dict["label_one_hot"] = raw_config["label"]["one_hot"]
# NOTE: I think the specification of final iteration shape/size should be
# defined in the preprocess function.. because there may be preprocess functions
# that need to happen before features/labels (if they even exist) are seperated.

# NOTE: not sure how I want to do this.. this basically becomes dataduit all
# over again..
# formatted_dict["TFR_dir"] = raw_config["TFR"]["dir"]
# formatted_dict["TFR_train"] = raw_config["TFR"]["train"]
# formatted_dict["TFR_test"] = raw_config["TFR"]["test"]
# formatted_dict["TFR_val"] = raw_config["TFR"]["validation"]

# # TODO: this is a first draft for this type of organization and will
# # will likely be changed
# formatted_dict["data_in_dict"] = raw_config["in"]
# formatted_dict["data_out_dict"] = raw_config["label"]
# formatted_dict["TFR_parse"] = raw_config["TFR_parse"]

# TODO: eventually, we need to support custom performance/loss metrics
performance = {"performance": {"objectives": performances_parser()}}
model = {
    "model": {
        # directory
        "name": categorical(
            default_value=None,
            required=True,
            is_type=str,
            description="model name `name: <str>`",
        ),
        "start_fresh": categorical(default_value=False, required=False, is_type=bool),
        "layers": layers_parser(),  # could add a check that the location exists
    }
}


DEFAULT_CONFIG = {}
DEFAULT_CONFIG = {**DEFAULT_CONFIG, **meta}
DEFAULT_CONFIG = {**DEFAULT_CONFIG, **performance}
DEFAULT_CONFIG = {**DEFAULT_CONFIG, **hyper_parameters}
DEFAULT_CONFIG = {**DEFAULT_CONFIG, **logging}
DEFAULT_CONFIG = {**DEFAULT_CONFIG, **data}
DEFAULT_CONFIG = {**DEFAULT_CONFIG, **model}
DEFAULT_CONFIG = {**DEFAULT_CONFIG, **optimize}
