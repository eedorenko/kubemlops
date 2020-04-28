import argparse
import dispatch_event_handler
import reg_model_event_handler

REGISTER_MODEL_EVENT = "Model is registered"


def get_event_handler(event_type):
    if (event_type == REGISTER_MODEL_EVENT):
        return reg_model_event_handler.RegModelEventHandler()
    else:
        return dispatch_event_handler.DispatchEventHandler()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--event_type',
                        help='Event Type')
    args = parser.parse_args()

    event_dispatcher = get_event_handler(args.event_type)
    event_dispatcher.dispatch() 