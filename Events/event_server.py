import sys
sys.path.insert(0, "..")
import logging

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

from opcua import ua, Server


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    logger = logging.getLogger("opcua.server.internal_subscription")
    logger.setLevel(logging.DEBUG)

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")

    # Creating a custom event: Approach 1
    # The custom event object automatically will have members from its parent (BaseEventType)
    etype = server.create_custom_event_type(idx, 'StopEvent', ua.ObjectIds.BaseEventType, [('Reason', ua.VariantType.String)])

    myevgen = server.get_event_generator(etype, myobj)

    # starting!
    server.start()

    try:
        # time.sleep is here just because we want to see events in UaExpert
        import time
        count = 0
        while True:
            time.sleep(5)
            myevgen.event.Message = ua.LocalizedText("Stop All Operations!")
            myevgen.event.Severity = count
            myevgen.event.Reason = "Button pushed"
            myevgen.trigger()
            count += 1

        embed()
    finally:
        # close connection, remove subcsriptions, etc
        server.stop()