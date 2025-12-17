# css定位参数化

# 登录界面
login_username = "#loginUsername input"
login_password = "#loginPasswd input"
login_commit = '#login'

## login_language
login_language = "button.header-user-btn"
language_choose_first = "div.t-dropdown__menu span:nth-child(1)"
language_choose_sencond = "div.t-dropdown__menu span:nth-child(2)"
language_choose_third = "div.t-dropdown__menu span:nth-child(3)"
language_choose_fourth = "div.t-dropdown__menu span:nth-child(4)"

## 向导界面
### 密码设置
guide_newpassword = "#loginPasswd input"
guide_Confirm_Password = "#confirmPassword input"
### wifi设置
guide_wlan_enable = "#wlanEnable"
guide_wlan_ssid = "#wlanCurrentSsidName input"
guide_wlan_password = "#wlanPassword input"
guide_wlan11ac_enable = "#wlan11acEnable"
guide_wlan11ac_ssid = "#wlan11acCurrentSsidName input"
guide_wlan11ac_password = "#wlan11acPassword input"
### 向导界面通用
guide_next = "#next"
guide_skip = "#skip"
guide_previous = "#previous"

#logout
logout = "#logout"
Comfirm = "button#confirm"
Cencel = "button#cancel"

#language
language = "div.t-menu div div:nth-child(3) button:nth-child(1)"
language_choose_first = "div.t-dropdown__menu span:nth-child(1)"
language_choose_sencond = "div.t-dropdown__menu span:nth-child(2)"
language_choose_third = "div.t-dropdown__menu span:nth-child(3)"
language_choose_fourth = "div.t-dropdown__menu span:nth-child(4)"

# home
## home 
Network = "#network"
DeviceName = "#deviceName"
DevicesInfo = "#devicesInfo"
home_one_line = ".t-table__row--hover"
home_one_line_td1 = '.t-table__row--hover td:nth-child(1)'
home_one_line_td2 = '.t-table__row--hover td:nth-child(2)'

# basic 
## wan
Basic_wan = model_base_url[model] + "/index.html#/basic/wan"   # url
wan_Enable = "#wanEnable"
wan_Connection_Status = "#wanConnectionStatus"
# 带下拉选项
wan_Request_Name = "#wanCurrentName input"
wan_Request_Name_TR069 = 'li[id*="TR069"]'
wan_Request_Name_INTERNET = 'li[id*="INTERNET"]'
wan_Request_Name_VOICE = 'li[id*="VOICE"]'
wan_Request_Name_OTHER = 'li[id*="OTHER"]'
# 带下拉选项
wan_Access_Type = "#wanWorkMode input"
wan_Access_Type_Route = 'li[id="Route"]'
wan_Access_Type_Bridge = 'li[id="Bridge"]'
# 带下拉选项
wan_Bearer_Service = "#wanService input"
wan_Bearer_Service_TR069 = 'li[title *=TR069]'
wan_Bearer_Service_INTERNET = 'li[title *=INTERNET]'
wan_Bearer_Service_HSI = 'li[title *=HSI]'
wan_Bearer_Service_VOICE = 'li[title *=VOICE]'
wan_Bearer_Service_VOIP = 'li[title *=VOIP]'
wan_Bearer_Service_OTHER = 'li[title *=OTHER]'
wan_Bearer_Service_IPTV = 'li[title *=IPTV]'
# 带下拉选项 当wanWorkMode选择路由模式
wan_Connection_Mode = "#wanConnectionMode input"
wan_Connection_Mode_DHCP = 'li[id="DHCP"]'
wan_Connection_Mode_Static = 'li[id="Static"]'
wan_Connection_Mode_PPPoE = 'li[id="PPPoE"]'
# 带下拉选项 当wanWorkMode选择桥模式
wan_Bridge_Mode = "#wanBridgeConnectionMode div.t-input"
wan_PPPoe_Bridge = "#PPPoE_Bridged"
wan_IP_Bridge = "#IP_Bridged"

### static 
wan_IP_Address = "#wanIpAddress input"
wan_Subnet_Mask = "#wanIpMask input"
wan_Default_Gateway = "#wanGatewayIp input"
wan_Primary_Dns = "#wanFirstDns input"
wan_Secondary_Dns = "#wanSecondDns input"
### pppoe
wan_pppoe_name = "#wanPppoeUsername input"
wan_pppoe_password = "#wanPppoePassword input"
# 带下拉选项
wan_VLAN_Gateway_Type = "#wanCurrentVlanMode input"
wan_VLAN_Gateway_Type_TAG = 'li[id = "TAG"]'
wan_VLAN_Gateway_Type_UNTAG = 'li[id="UNTAG"]'
wan_VLAN_Gateway_Type_TRANSPARENT = 'li[id="TRANSPARENT"]'
wan_VLAN_ID = "#wanVlanId input"
wan_MTU = "#wanMtu input"
### IPv4&IPV6
wan_ipv4 = 'label#IPv4 span[class="t-radio__input"]'
wan_ipv4ipv6 = 'label.t-radio[id="IPv4/IPv6"] span[class="t-radio__input"]'
# 带下拉选项
wan_IPv6_Connection_Mode = "#wanIpv6ConnectionMode input"
wan_IPv6_Connection_Mode_SLAAC = 'li[id="SLAAC"]'
wan_IPv6_Connection_Mode_DHCP = 'li[id="DHCP"]'
wan_IPv6_Connection_Mode_Static = 'li[id="Static"]'
# ipv6
wan_IPv6_Address = "#wanIpV6Address input"
wan_IPv6_Prefix_Length = "#wanIpV6PrefixLe input"
wan_IPv6_Gateway = "#wanIpv6Gateway input"
wan_IPV6_Primary_DNS = "#wanIpv6FirstDns input"
wan_IPv6_Secondary_DNS = "#wanIpv6SecondDns input"
wan_IPv6_Prefix_Address = "#wanIpv6PdPrefixAddress input"
wan_IPv6_Primary_Time = "#wanIpv6PdPrefixPrimaryTime input"
wan_IPv6_Lease_Time = "#wanIpv6PdPrefixLeaseTime input"
wan_commit = "#wanSavelButton"

## lan
Basic_lan = model_base_url[model] + "/index.html#/basic/lan"  # url
lan_LAN_IP= "#lanIpv4Address input"
lan_Subnet_Mask= "#lanIpv4Mask input"
lan_DHCP_Server = "#dhcpEnable"
lan_IP_Start = "#lanIpv4AddrStart input"
lan_IP_End = "#lanIpv4AddrEnd input"
lan_commit = "#saveButton"
lan_RA_Enable = "#lanIpv6RadvdEnable"
lan_DHCPv6_Server = "#lanIpv6DhcpEnable"
lan_IPV6_commit = "#lanIpv6SaveButton"

## CWMP
Basic_cwmp = model_base_url[model] + "/index.html#/basic/cwmp"
cwmp_Periodic_Notification_Enable = "#cwmpPeriodEnable"
cwmp_Notification_Interval = "#cwmpPeriodInterval input"
cwmp_Server_URL = "#cwmpAcsUrl input"
cwmp_Platform_Username = "#cwmpAcsUserName input"
cwmp_Platform_Password = "#cwmpAcsPassWord input"
cwmp_Terminal_Username = "#cwmpClientReqUserName input"
cwmp_Terminal_Password = "#cwmpClientReqPassWord input"
cwmp_commit = "#cwmpSaveButton"

## voip
Basic_voip = model_base_url[model] + "/index.html#/basic/voip"
## basic setting
voip_Protocol = "#voipCurrentProtocol input"
voip_Binding_Interface = "#voipCurrentInterface input"
voip_Region = "#voipRegion input"
voip_Register_Server = "#voipRegisterServer input"
voip_Proxy_Server = "#voipProxyServer input"
voip_Proxy_Server_port = "#voipProxyServerPort input"
voip_Outbound_Proxy = "#voipOutboundProxyServer input"
voip_Outbound_Proxy_port = "#voipOutboundProxyServerPort input"
voip_Secondary_Register_Server = "#voipSecRegisterServer input"
voip_Secondary_Proxy_Server = "#voipSecProxyServer input"
voip_Secondary_Proxy_Server_port = "#voipSecProxyServerPort input"
voip_Secondary_Outbound_Proxy = "#voipSecOutboundProxyServer input"
voip_Secondary_Outbound_Proxy_port = "#voipSecOutboundProxyServerPort input"
voip_Registration_Status= "#voipRegistrationStatus"
voip_Port_Rnable = "#voipPortEnable"
voip_Account = "#voipAccount"
voip_Password = "#voipPassword"
voip_commit = "#voipBasicSave"

## IPTV
Basic_iptv = model_base_url[model] + "/index.html#/basic/iptv"
iptv_Enable = "#multicastEnable"
iptv_Bind_Option_LAN1 = '#LAN1 span[class="t-checkbox__input"]'
iptv_Bind_Option_LAN2 = '#LAN2 span[class="t-checkbox__input"]'
iptv_Bind_Option_LAN3 = '#LAN3 span[class="t-checkbox__input"]'
iptv_Bind_Option_LAN4 = '#LAN4 span[class="t-checkbox__input"]'
iptv_Access_Type = "#multicastMode input"
iptv_Multicast_VLAN_ID = "#multicastVlanId input"
iptv_commit = "#iptvSaveButton"
iptv_IGMPMLD_Snooping = "#igmpSnoopingEnable"
iptv_IGMPMLD_Proxy = "#igmpProxyEnable"

## bandsteering
Basic_bandsteer = model_base_url[model] + "/index.html#/basic/wifi/bandsteer"
bandsteering_enable = "#wifiband"
bandsteering_SSID = "#bnadSteeringSsid input"
bandsteering_Encryption = "#bnadSteeringCurrentEntrypt input"
bandsteering_Password = "#bnadSteeringPassword input"
bandsteering_24G_to_5G_RSSI = "#bnadSteering2GTo5GRssi input"
bandsteering_5G_to_24G_RSSI = "#bnadSteering5GTo2GRssi input"
bandsteering_commit = "#bnadSteeringSave"
##2.4G wifi
Basic_wifi_24G = model_base_url[model] + "/index.html#/basic/wifi/wifi24"
wlan_Enable = "#bandSteeringEnable"
wlan_SSID = "#wlanCurrentSsidName input"
wlan_more_wifi = "#wifi24ShowMoreAp"
wlan_Encryption = "#wlanCurrentEntrypt input"
wlan_Password = "#wlanPassword input"
wlan_WPA_Encription = "#wlanWpaEncription input"
wlan_more_setting = '#moreSettings div[class="t-collapse-panel__header t-is-clickable"]'
wlan_Select_Mode = "#wlanCurrentMode input"
wlan_Bandwidth = "#wlanCurrentBandwidth input"
wlan_Country = "#wlanCountry input"
wlan_Wireless_Channel = "#wlanCurrentChannel input"
wlan_get_score = "#wifiScan"
wlan_Signal_Strength = "#wlanCurrentSignal input"
wlan_commit = "#wlanSave"
## 5G wifi
Basic_wifi_5G = model_base_url[model] + "/index.html#/basic/wifi/wifi5"
wlan11ac_Enable = "#bandSteeringEnable"
wlan11ac_SSID = "#wlan11acCurrentSsidName input"
wlan11ac_more_wifi = "#wifi24ShowMoreAp"
wlan11ac_Encryption = "#wlan11acCurrentEntrypt input"
wlan11ac_Password = "#wlan11acPassword input"
wlan11ac_WPA_Encription = "#wlan11acWpaEncription input"
wlan11ac_more_setting = '#moreSettings div[class="t-collapse-panel__header t-is-clickable"]'
wlan11ac_Select_Mode = "#wlan11acCurrentMode input"
wlan11ac_Bandwidth = "#wlan11acCurrentBandwidth input"
wlan11ac_Country = "#wlan11acCountry input"
wlan11ac_Wireless_Channel = "#wlan11acCurrentChannel input"
wlan11ac_get_score = "#wifiScan"
wlan11ac_Signal_Strength = "#wlan11acCurrentSignal input"
wlan11ac_commit = "#wlan11acSave"

## WPS
Basic_wifi_wps = model_base_url[model] + "/index.html#/basic/wifi/wps"
wps_enable = "#wpsTrigger"

## Guest
Basic_wifi_guest = model_base_url[model] + "/index.html#/basic/wifi/guest"
guest_Guest_2G_Enable = "#guestWifi2GEnable"
guest_Guest_2G_SSID = "#guestWifi2GSsidName input"
guest_Guest_2G_Password = "#guestWifi2GPassword input"
guest_Guest_2G_MaxStaNum = "#guestWifi2GDeviceCount input"
guest_Guest_5G_Enable = "guestWifi5GEnable"
guest_Guest_5G_SSID = "#guestWifi5GSsidName input"
guest_Guest_5G_Password = "#guestWifi5GPassword input"
guest_Guest_5G_MaxStaNum = "#guestWifi5GDeviceCount input"
guest_commit = "#guestWifiSave"

## access devices
Basic_access_devices = model_base_url[model] + "/index.html#/basic/device"

## Parental Control
Basic_Parental_Control = model_base_url[model] + "/index.html#/basic/parentalControl"
Parental_Control_enable = "#parentalEnableStatus"
Parental_Control_add = "#parentalAdd"
Parental_Control_rule_mac_input = "#mac"
Parental_Control_rule_mac_add = "#onAddMac"
Parental_Control_rule_select_device = "#onChooseDevice"
Parental_Control_rule_parentalCtlDurationActive = "#parentalCtlDurationActive"
Parental_Control_rule_start_time = "#starttime0 input"
Parental_Control_rule_end_time = "#endtime0 input"
Parental_Control_rule_selete_wek = "#week0 input"
Parental_Control_rule_add_time = "#addTime"
Parental_Control_rule_parentalCtlActiveUrl = "#parentalCtlActiveUrl"
Parental_Control_rule_Black_list = "#Black span.t-radio__input"
Parental_Control_rule_White_list = "#White span.t-radio__input"
Parental_Control_rule_list_address0 = "#addressItem0"
Parental_Control_rule_cancel = "#cancel"
Parental_Control_rule_commit = "#save"

## Operate Mode
Basic_Operate_Mode = model_base_url[model] + "/index.html#/basic/mode"
mode_Gpon = "#modeGPON"
mode_Epon = "#modeEPON"

## Eazymesh
Basic_Easymesh = model_base_url[model] + "/index.html#/basic/EasyMesh"
Eazymesh_EasyMesh = "#meshEnable"
Eazymesh_Map_Version = "#meshVersion"
Eazymesh_Device_Role = "#meshRole input"
Eazymesh_Steering = "#steerEnable"
Eazymesh_Load_Default_Setting = "#reset"
Eazymesh_Trigger_WIFI_On_boarding = "#meshTrigger"
Eazymesh_commit = "#meshSaveButton"

# Advanced
## Speed Test
Advanced_Speed_Test = model_base_url[model] + "/index.html#/basic/EasyMesh"
Speed_Test_start = "#startTest"

##Qos
Advanced_netword_qos = model_base_url[model] + "/index.html#/advanced/network/qos"
Qos_Rule_Template = "#qosMode input"
Qos_Enable_QoS = "#qosEnable"
Qos_Uplink_Bandwidth = "#qosUplinkBandwidth input"
Qos_Enable_DSCP_Flag = "#qosDscp"
Qos_Enable_8021P_Flag = "#qosEn8021PRemark input"
Qos_Select_type_Dics = '#discRule span[class="t-radio__input"]'
Qos_Select_type_VLANID = '#vlanidRule span[class="t-radio__input"]'
Qos_Select_type_App = '#appRule span[class="t-radio__input"]'
Qos_Select_type_Type = '#typeRule span[class="t-radio__input"]'
Qos_Scheduling_policy_PQ = "#PQ span.t-radio__input"
Qos_Scheduling_policy_WRR = "#WRR span.t-radio__input"
Qos_Scheduling_policy_CAR = "#CAR span.t-radio__input"
# disc+Wrr模式
Qos_Scheduling_qosEnableForceWeight = "#qosEnableForceWeight"
# app或type模式
Qos_app_add_rule = "#appRuleAdd"

## Port Binding
Advanced_netword_binding = model_base_url[model] + "/index.html#/advanced/network/binding"

## LAN Port Mode
Advanced_netword_lanPort = model_base_url[model] + "/index.html#/advanced/network/lanPort"
lan1_speed = "#port1Speed"
lan1_mode = "#port1Mode"
lan2_speed = "#port2Speed"
lan2_mode = "#port2Mode"
lan3_speed = "#port3Speed"
lan3_mode = "#port3Mode"
lan4_speed = "#port4Speed"
lan4_mode = "#port4Mode"
lan_port_commit = "#lanPortSaveButton"

## FTP Client
Advanced_FTP_Client = model_base_url[model] + "/index.html#/advanced/network/ftpClient"
Ftp_client_USB_Connect_Status = "#ftpClientUsbConnectStatus"
Ftp_client_Download_Progess = "#ftpDownloadProgress"
Ftp_client_Download_URL = "#ftpClientDownloadUrl input"
Ftp_client_USB_Interface_Name = "#ftpClientUsbInterfaceName input"
Ftp_client_Auth_Enable = "#ftpClientAuthEnable"
Ftp_client_username = "#ftpDownloadName input"
Ftp_client_password = "#ftpDownloadPassword input"
Ftp_client_commit = "#ftpDownSaveButton"

## Vpn
### ipSec
Advanced_Vpn_ipSec = model_base_url[model]  + "/index.html#/advanced/network/vpn/ipSec"
vpn_add = "#vpnAddButton"
vpn_rule_Connection_Name = "#vpnConnectionName input"
vpn_rule_Local_Gateway_IP = "#vpnLocalGatewayIp input"
vpn_rule_Remote_Gateway_IP = "#vpnRemoteGatewayIp input"
vpn_rule_Local_Access_Range = "#vpnLocalAccessRange input"
vpn_rule_Local_IP_Address = "#vpnLocalIpAddress input"
vpn_rule_Local_SubnetMask = "#vpnLocalIpSubnetMask input"
vpn_rule_Remote_Access_Range = "#vpnRemoteAccessRange input"
vpn_rule_Remote_IP_Address = "#vpnRemoteIpAddress input"
vpn_rule_Remote_SubnetMask = "#vpnRemoteIpSubnetMask input"
vpn_rule_Pre_Shared_Key = "#vpnPreSharedKey input"
vpn_rule_Perfect_Forward_Secrecy = "#vpnPerfectForwardSecrecy"
vpn_rule_Exchange_Mode_Phase_1 = "#vpnExchangeMode input"
vpn_rule_Encryption_Algorithm_Phase_1 = "#vpnKey1EncryptionAlgorithm input"
vpn_rule_Authentication_Algorithm_Phase_1 = "#vpnKey1AuthenticationAlgorithm input"
vpn_rule_Diffie_Hellman_Group_Phase_1 = "#vpnKey1DiffieHellmanGroup input"
vpn_rule_Key_Life_Time_Phase_1 = "#vpnKey1LifeTime input"
vpn_rule_Key_Life_Time_type_Phase_1 = "#vpnKey1LifeTimeType input"
vpn_rule_Encryption_Algorithm_Phase_2 = "#vpnKey1EncryptionAlgorithm input"
vpn_rule_Authentication_Algorithm_Phase_2 = "#vpnKey1AuthenticationAlgorithm input"
vpn_rule_Diffie_Hellman_Group_Phase_2 = "#vpnKey2DiffieHellmanGroup input"
vpn_rule_Key_Life_Time_Phase_2 = "#vpnKey2LifeTime input"
vpn_rule_Key_Life_Time_type_Phase_2 = "#vpnKey2LifeTimeType input"
vpn_rule_cancel = "button.t-dialog__cancel"
vpan_rule_commit = "button.t-dialog__confirm"

## Upnp
Advanced_Network_upnp = model_base_url[model] +  "/index.html#/advanced/network/upnp"
Upnp_enable = "#upnpEnable"
Upnp_disable_cancel = "button#cancel"
Upnp_disable_confirm = "button#confirm"

## Smaba
Advanced_Network_samba = model_base_url[model] + "/index.html#/advanced/network/samba"
Smaba_enable = "#sambaEnable"
Smaba_Username = "#sambaUserName input"
Smaba_New_Password = "#sambaNewPasswd input"
Smaba_Confirm_Password = "#sambaConfirmPasswd input"
Smaba_Work_Group = "#sambaWorkGroup input"
Smaba_Net_Bios_Name = "#sambaNetBiosName input"
Smaba_commit = "#sambaSaveButton"
Smaba_reset = "#sambaResetButton"

## DDNS
Advanced_Network_Ddns= model_base_url[model] + "/index.html#/advanced/network/DDNS"
Ddns_add_rule = "div.addButton>button"
Ddns_rule_Provider = "#ddnsName input"
Ddns_rule_Server_Port = "#ddnsSserverPort input"
Ddns_rule_Host = "#ddnsHostName input"
Ddns_rule_Domain = "#ddnsDomain input"
Ddns_rule_Username = "#ddnsUsername input"
Ddns_rule_Password = "#ddnsPassword input"
Ddns_rule_Enbale = "#ddnsEnabled"
Ddns_rule_cancel = "#ddnsCancelButton"
Ddns_rule_Commit = "#ddnsSaveButton"

## Static Route
Advanced_Network_Static_Route = model_base_url[model] + "/index.html#/advanced/network/staticRoute"
Static_Route_add_rule = "#route4AddButton"
Static_Route_rule_IP_Address = "#ipv4StaticRouterAddr input"
Static_Route_rule_Gateway = "#ipv4StaticRouterGateway iput"
Static_Route_rule_Subnet_Mask = "#ipv4StaticRouterMask input"
Static_Route_rule_Interface = "#ipv4StaticRouterInterface input"
Static_Route_rule_cancel = "div#ipv4StaticRouterInfo div.t-dialog button:nth-child(1)"
Static_Route_rule_commit = "div#ipv4StaticRouterInfo div.t-dialog button:nth-child(2)"

## firewall
Advanced_User_Firewall = model_base_url[model] + "/index.html#/advanced/user/Firewall"
Firewall_enable_or_disable = "div#enablefire"
Firewall_Attack_protection = "#enablefire"
Firewall_Security_Level = "#firewallLevel input"
Firewall_disable_cancel = "button#cancel"
Firewall_disable_confirm = "button#confirm"

## MAC Filter
Advanced_User_MAC_Filter = model_base_url[model] + "/index.html#/advanced/user/macFilter"
mac_filter_enable_or_disable = "#macFilterEnable"
mac_filter_disable_cancel = "button#cancel"
mac_filter_disable_confirm = "button#confirm"
mac_filter_add_rule = "#macFilterAddButton"
mac_filter_rule_device_name = "#macFilterName input"
mac_filter_rule_mac = "#macAddress input"
mac_filter_rule_cancel = "button.t-dialog__cancel"
mac_filter_rule_commit = "button.t-dialog__confirm"

## URL Filter
Advanced_User_URL_Filter = model_base_url[model] + "/index.html#/advanced/user/urlFilter"
url_filter_enable_or_disable = "#urlFilterEnable"
url_filter_disable_cancel = "button#cancel"
url_filter_disable_confirm = "button#confirm"
url_filter_add_rule = "#urlFilterAddButton"
url_filter_rule_url = "#urlFilterUrl input"
url_filter_rule_cancel = "button.t-dialog__cancel"
url_filter_rule_commit = "button.t-dialog__confirm"

## ACl
Advanced_User_ACL_Filter = model_base_url[model] + "/index.html#/advanced/user/aclFilter"
Acl_filter_enable_or_disable = "#aclEnable"
Acl_filter_disable_cancel = "button#cancel"
Acl_filter_disable_confirm = "button#confirm"
Acl_filter_add_rule = "#aclAddButton"
Acl_filter_rule_Enable = "#aclEntryEnable"
Acl_filter_rule_Filter_Name = "#aclName input"
Acl_filter_rule_Src_IP_Start = "#aclSrcIPStart input"
Acl_filter_rule_Src_IP_End = "#aclSrcIPEnd input"
Acl_filter_rule_Application = "#aclApplication input"
Acl_filter_rule_Interface = "#aclInterface input"
Acl_filter_rule_cancel = "button.t-dialog__cancel"
Acl_filter_rule_commit = "button.t-dialog__confirm"

## portFilter
Advanced_User_portFilter = model_base_url[model] + "/index.html#/advanced/user/portFilter"
### up filter
portFilter_up_enable_or_disable = "#upFilterEnable"
portFilter_up_disable_cancel = "button#cancel"
portFilter_up_disable_confirm = "button#confirm"
portFilter_up_add_rule = "#upFilterAddButton"
portFilter_up_rule_Name = "#upPortFilterRuleName input"
portFilter_up_rule_Protocol = "#upPortFilterProtocol input"
portFilter_up_rule_Source_Address = "#upPortFilterSrcIpAddress input"
portFilter_up_rule_Source_Subnet_Mask = "#upPortFilterSrcMask input"
portFilter_up_rule_Source_Port = "#upPortFilterSrcPort input"
portFilter_up_rule_Destination_Address = "#upPortFilterDestIpAddress input"
portFilter_up_rule_Destination_Subnet_Mask = "#upPortFilterDestIpMask input"
portFilter_up_rule_Destination_Port = "#upPortFilterDestPort input"
portFilter_up_rule_cancel = "button#upPortFilterCanelButton"
portFilter_up_rule_commit = "button#upPortFilterSaveButton"
### down filter
portFilter_down_enable_or_disable  = "#downFilterEnable"
portFilter_down_disable_cancel = "button#cancel"
portFilter_down_disable_confirm = "button#confirm"
portFilter_down_add_rule = "#downFilterAddButton"
portFilter_down_rule_Name = "#downPortFilterRuleName input"
portFilter_down_rule_Protocol = "#downPortFilterProtocol input"
portFilter_down_rule_Source_Address = "#downPortFilterSrcIpAddress input"
portFilter_down_rule_Source_Subnet_Mask = "#downPortFilterSrcMask input"
portFilter_down_rule_Source_Port = "#downPortFilterSrcPort input"
portFilter_down_rule_Destination_Address = "#downPortFilterDestIpAddress input"
portFilter_down_rule_Destination_Subnet_Mask = "#downPortFilterDestIpMask input"
portFilter_down_rule_Destination_Port = "#downPortFilterDestPort input"
portFilter_down_rule_Interface = "#downPortFilterInterface input"
portFilter_down_rule_cancel = "button#downPortFilterCancelButton"
portFilter_down_rule_commit = "button#downPortFilterSaveButton"


##Port Forward
Advanced_User_portForward = model_base_url[model] + \
    "/index.html#/advanced/user/portForward"
Port_Forward_add_rule = "#portForwardAddButton"
Port_Forward_rule_Application = "#curApplication input"
Port_Forward_rule_Protocol = "#portMappingProtocol input"
Port_Forward_rule_External_Port = "#externalPort input"
Port_Forward_rule_Internal_Port = "##internalPort input"
Port_Forward_rule_Internal_Host = "##internalPort input"
Port_Forward_rule_Mapping_Name = "#mappingName input"
Port_Forward_rule_cancel = "#cancelButton"
Port_Forward_rule_commit = "#saveButton"

## DMZ
Advanced_User_DMZ = model_base_url[model] + "/index.html#/advanced/user/dmz"
Dmz_enable_or_disable = "#dmzEnable"
Dmz_Host_IP_Address = "#dmzIpaddress input"
Dmz_commit = "#dmzSave"

## ALG
Advanced_User_ALG = model_base_url[model] + "/index.html#/advanced/user/alg"
Enable_L2TP_Alg = '#algL2TP span[class="t-checkbox__input"]'
Enable_IPSec_Alg = '#algIPSEC span[class="t-checkbox__input"]'
Enable_H323_Alg = '#algH323 span[class="t-checkbox__input"]'
Enable_RTSP_Alg = '#algRTSP span[class="t-checkbox__input"]'
Enable_SIP_Alg = '#algSIP span[class="t-checkbox__input"]'
Enable_FTP_Alg = '#algFTP span[class="t-checkbox__input"]'
Enable_PPTP_Alg = '#algPPTP span[class="t-checkbox__input"]'
Alg_commit = "#ALG"


## password
Advanced_System_Password_Management = model_base_url[model] + "/index.html#/advanced/system/password"
Password_Management_Username = "#loginUsername input"
Password_Management_New_Password = "#newPassword input"
Password_Management_Confirm_Password = "#confirmPassword input"
Password_Management_commit = "#saveButton"

## Upgrade
Advanced_System_Upgrade = model_base_url[model] + "/index.html#/advanced/system/upgrade"
Upgrade_Local_Upgrade = ".t-upload input"
Upgrade_commit = "#update"

## Device Management
Advanced_System_Upgrade = model_base_url[model] + "/index.html#/advanced/system/device"
Device_Management_Upgrade = "#upload button"
Device_Management_Import_File = "#importRomButton"
Device_Management_ROM_Backup = "#importRomButton"
Device_Management_Restart ="#reboot"
Device_Management_Reset = "#reset"

## LED Control
Advanced_System_LED_Control = model_base_url[model] + "/index.html#/advanced/system/ledCtrl"
Led_enable_or_disable = "#ledCtrlEnable"
Led_disable_cancel = "button#cancel"
Led_disable_confirm = "button#confirm"

## System Test
Advanced_System_System_Test = model_base_url[model] + "/index.html#/advanced/system/test"
System_Test_Ping_Repeat_Times = "#diagnosePingTimes input"
System_Test_Ping_Interface = "#diagnosePingInterface input"
# 下拉选项
System_Test_Ping_Interface_TR069 = 'li[id*="TR069"]'
System_Test_Ping_INTERNET = 'li[id*="INTERNET"]'
System_Test_Ping_VOICE = 'li[id*="VOICE"]'
System_Test_Ping_OTHER = 'li[id*="OTHER"]'
System_Test_Ping_Address = "#diagnosePingAddess input"
System_Test_Ping_Start = "#pingStartButton"
System_Test_Tracert = "#diagnoseTracertInterface input"
System_Test_Tracert = "#diagnoseTracertAddess input"
System_Test_Tracert_Start = "#tracertStartButton"
System_Test_Manual_Report = "#informButton"

## Timeset
Advanced_System_Timeset = model_base_url[model] + "/index.html#/advanced/system/timeSetting"
Timeset_Automatic = "#automatic"
Timeset_Master_Sntp_Server = "#timeSettingSntpServer1 input"
Timeset_Slave_Sntp_Server = "#timeSettingSntpServer2 input"
Timeset_Sync_Interval = "#timeSettingInterval input"
Timeset_Time_Zone = "#timeSettingZone input"
Timeset_commit = "#timeSettingSaveButton"

## logManage
Advanced_System_logManage = model_base_url[model] + "/index.html#/advanced/system/logManage"
LogManage_enable_or_disable = "#systemLogEnable"
LogManage_enable_confirm = "button#confirm"
LogManage_Log_Level = "#systemLogLevel input"
LogManage_download = "#downloadButton"

## Timed Reboot
Advanced_System_Timed_Reboot = model_base_url[model] + "/index.html#/advanced/system/autoReboot"
Timed_Reboot = "#autoRebootEnable"
Timed_Reboot_Sun = "div.t-checkbox-group > label: nth-child(1) span"
Timed_Reboot_Mon = "div.t-checkbox-group > label: nth-child(2 span"
Timed_Reboot_Tues = "div.t-checkbox-group > label: nth-child(3) span"
Timed_Reboot_Wed = "div.t-checkbox-group > label: nth-child(4) span"
Timed_Reboot_Thur = "div.t-checkbox-group > label: nth-child(5) span"
Timed_Reboot_Fri = "div.t-checkbox-group > label: nth-child(6) span"
Timed_Reboot_Fri = "div.t-checkbox-group > label: nth-child(7) span"
Timed_Reboot_Time = "#autoRebootTime input"
Timed_Reboot_commit = "#autoRebootSaveButton"

## PON Auth
Advanced_System_PON_Auth = model_base_url[model] + "/index.html#/advanced/system/ponAuth"
PON_Auth_Mode = "#ponCurrentAuth input"
### loid 模式
PON_Loid = "#ponLoid input"
PON_Loid_Password = "#ponLoidPasswd input"
### pwd模式
PON_Password = "#ponPassword"
PON_Auth_commit = "#ponAuthSaveButton"

## Tool
Advanced_System_Tool = model_base_url[model] + "/index.html#/advanced/system/tool"
Tool_telnetEnable = "#telnetEnable"
Tool_wanMirrorEnable = "#wanMirrorEnable"


# hidepage
hidepage_login_url = model_base_url[model] + "/#/hidePage"
hidepage_login_username = "#hidePageUsername input"
hidepage_login_password = "#hidePagePassword input"
hidepage_login_commit = "#hidePageLoginButton"
## hidepage Common Setting
hidepage_telnetEnable = "#telnetEnable"
hidepage_wanMirrorEnable = "#wanMirrorEnable"
## hidepage Common Setting
hidepage_Upgrade_Local_Upgrade = '.t-upload button'
hidepage_Upgrade_commit = "#update"
## hidepage Password Management
hidepage_Username = "#loginUsername input"
hidepage_New_Password = "#newPassword input"
hidepage_Confirm_Password = "#confirmPassword input"
hidepage_Password_Management_commit = "#saveButton"
## hidepage Device Management
hidepage_Device_Management_Upgrade = "#upload button"
hidepage_Device_Management_Import_File = "#importRomButton"
hidepage_Device_Management_ROM_Backup = "#importRomButton"
hidepage_Device_Management_Restart = "#reboot"
hidepage_Device_Management_Reset = "#reset"
