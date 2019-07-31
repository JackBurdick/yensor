import tensorflow as tf
import os
import numpy as np
from typing import Any

from yeahml.dataset.handle_data import return_batched_iter  # datasets from tfrecords
from yeahml.log.yf_logging import config_logger  # custom logging
from yeahml.build.components.metrics import get_metrics_fn
from yeahml.build.components.loss import get_loss_fn


@tf.function
def eval_step(model, x_batch, y_batch, loss_fn, loss_avg, metric_fns):
    prediction = model(x_batch)
    loss = loss_fn(y_batch, prediction)

    # NOTE: only allow one loss
    loss_avg(loss)

    # TODO: ensure pred, gt order
    for eval_metric_fn in metric_fns:
        eval_metric_fn(prediction, y_batch)


def eval_model(model: Any, MCd: dict, weights_path: str = None) -> dict:

    logger = config_logger(MCd, "eval")

    # load best weights
    # TODO: load specific weights according to a param
    if weights_path:
        specified_path = weights_path
    else:
        specified_path = MCd["save_weights_path"]
    model.load_weights(specified_path)
    logger.info("params loaded from {}".format(specified_path))

    # loss
    # get loss function
    loss_object = get_loss_fn(MCd["loss_fn"])

    # mean loss
    avg_eval_loss = tf.keras.metrics.Mean(name="validation_loss", dtype=tf.float32)

    # metrics
    eval_metric_fns, metric_order = [], []
    for metric in MCd["met_set"]:
        eval_metric_fn = get_metrics_fn(metric)
        metric_order.append(metric)
        eval_metric_fns.append(eval_metric_fn)

    # reset metrics (should already be reset)
    for eval_metric_fn in eval_metric_fns:
        eval_metric_fn.reset_states()

    # get datasets
    tfr_eval_path = os.path.join(MCd["TFR_dir"], MCd["TFR_train"])
    eval_ds = return_batched_iter("eval", MCd, tfr_eval_path)

    logger.info("-> START evaluating model")
    for step, (x_batch, y_batch) in enumerate(eval_ds):
        eval_step(model, x_batch, y_batch, loss_object, avg_eval_loss, eval_metric_fns)
    logger.info("[END] evaluating model")

    logger.info("-> START creating eval_dict")
    eval_dict = {}
    for i, name in enumerate(metric_order):
        cur_metric_fn = eval_metric_fns[i]
        eval_dict[name] = cur_metric_fn.result().numpy()
    logger.info("[END] creating eval_dict")

    # TODO: log each instance

    return eval_dict
