from opcua import Server, ua, uamethod, Client
import os, time
from OurProductDataType_Lib import OurProduct

@uamethod
def storageReceived(parent, new_product):
    print(new_product)
    return "OK"
    
@uamethod
def storageCheck(parent):
    print("Check")
    return True

@uamethod
def storagePass(parent, new_product):
    print(new_product)
    return "OK"

class OPCUA_Server(OurProduct):
    def __init__(self, endpoint, name):
        #Configuration
        print("Init", name, "...")
        self.name = name
        self.server = Server ()
        self.my_namespace_name = 'http://hs-emden-leer.de/OurProduct/'
        self.my_namespace_idx = self.server.register_namespace(self.my_namespace_name)
        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)
       
        #Add new object - MyModule
        self.objects = self.server.get_objects_node()
        self.fstorage = self.objects.add_object(self.my_namespace_idx, "ForStorage")
        
        #
        #pass in argument(s)
        self.create_our_product_type()
        inarg_ourproduct = ua.Argument()
        inarg_ourproduct.Name = "OurProduct"
        inarg_ourproduct.DataType = self.ourproduct_data.data_type
        inarg_ourproduct.ValueRank = -1 
        inarg_ourproduct.ArrayDimensions = []
        inarg_ourproduct.Description = ua.LocalizedText("A new Product")

        #pass out argument 
        outarg_answer = ua.Argument()
        outarg_answer.Name = "Answer"
        outarg_answer.DataType = ua.NodeId(ua.ObjectIds.String)
        outarg_answer.ValueRank = -1 
        outarg_answer.ArrayDimensions = []
        outarg_answer.Description = ua.LocalizedText("Here you can specify an answer")
        
        
        self.fstorage.add_method(self.my_namespace_idx, "storagePass", storagePass, [inarg_ourproduct], [outarg_answer])
        self.fstorage.add_method(self.my_namespace_idx, "storageReceived", storageReceived, [inarg_ourproduct], [outarg_answer])
       
        #check answer
        outarg = ua.Argument()
        outarg.Name = "Answer"
        outarg.DataType = ua.NodeId(ua.ObjectIds.Boolean)
        outarg.ValueRank = -1 
        outarg.ArrayDimensions = []
        outarg.Description = ua.LocalizedText("Here you can specify an answer")
        
        #check methods
        self.fstorage.add_method(self.my_namespace_idx, "storageCheck", storageCheck, [], [outarg])
       
        
    def __enter__(self) :
        #Start server
        print("Setup", self.name, "....")
        self.server.start()
        return self
    
    def __exit__(self, exc, exc_val, exc_tb) :
        #Close server
        print("Closing", self.name, "....")
        self.server.stop()

class Storage_Client():
    
    def __init__(self, endpoint):
        self.client = Client(endpoint)
      
    def __enter__(self):
        while(True):
            try:
                self.client.connect()
                print("Storage client connected")
                break
            except:
                print("Failed to connect Storage client")
                time.sleep(0.5)
        

        self.mynamespace_idx = self.client.get_namespace_index("http://hs-emden-leer.de/OurProduct/")
        self.root = self.client.get_root_node()
        self.sobj = self.root.get_child(["0:Objects", "{}:warehouse".format(self.mynamespace_idx)])
        self.client.load_type_definitions() 

        return self


    def askIsFree(self):
        res = self.sobj.call_method("{}:storageCheck".format(self.mynamespace_idx))
        print("Receive answer is: ", res)
        return res
     
 
    def passPiece(self,piece):
        res = self.sobj.call_method("{}:storageReceived".format(self.mynamespace_idx),piece)
        print("Receive answer is: ", res)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Disconnecting....")
        self.client.disconnect()
        

if __name__ == '__main__' :

    server_name = "TransportServer"
    endpoint_address = "opc.tcp://127.0.0.2:40840"
    sadress = "opc.tcp://192.168.178.81:51319"
    
    tserv = OPCUA_Server(endpoint_address, server_name)
    
    sclient = Storage_Client(sadress)
    
    with tserv:
        try:
            while True:
                time.sleep(0.5)


        except KeyboardInterrupt:
            print("Goodbye")