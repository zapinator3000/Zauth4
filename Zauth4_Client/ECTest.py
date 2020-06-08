import EasyConnections as EC
Conn=EC.Connections()
Conn.app_key="rmdVHkrUUbiK96gKc14zTm3Et_AJq5YTKIu5jVQYTrk="
Conn.init_debug("gAAAAABcMQwte8bXXvhECACNIRt2HyE6byKOkj6VRPl0SYDAzfe75pqthR2INeT43h_WB3TLM1xA8_J3WbN3sk-23vwChtI2vRg2DtR66w1LBkd-qNyJT_a92O6pOS7x11pWhLYlK_1c","rmdVHkrUUbiK96gKc14zTm3Et_AJq5YTKIu5jVQYTrk=")
Conn.test_system()
Conn.send_special("Zauth_Dev.zauth","Zauth_Dev.zauth")
Conn.login_wrapper("Test App")
Conn.close()
input("Press Enter to Continue")
