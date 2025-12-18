# element_config.py
# 基于实际 HTML 结构重构，命名统一、覆盖全面、定位精准

base_url = "http://192.168.10.1"
login_username = "admin"
login_password = "admin"

# ========================
# 🔐 登录界面
# ========================
login_page = base_url + "/index.html"
login_username_field = 'input[placeholder="Please Enter Your Username"]'
login_password_field = 'input[placeholder="Please Enter Your Password"]'
login_submit_button = "button[type='submit']"  # 或者根据文本

# ========================
# 🏠 首页 / Home
# ========================
home_page = base_url + "/index.html"
home_network_status = "#network"
home_device_name = "#deviceName"
home_connected_devices = "#devicesInfo"
home_device_table_row = ".t-table__row--hover"

# ========================
# 🏠 Home - Status Pages (SPA)  这里需要xPATH定位
# ========================
# --- 顶部导航图标 ---
network_icon = 'span[id="network"]'  # Network 图标
router_icon = 'span[id="deviceName"]'  # FT-35 图标
device_icon = 'span[id="devicesInfo"]'  # Device 图标

# --- Network 下的标签页 ---
connect_info_tab = "//span[contains(text(), 'Connect Information')]"
eth_port_info_tab = "//span[contains(text(), 'Eth Port Information')]"
wifi_info_tab = "//span[contains(text(), 'WiFi Information')]"

# --- IPv4 连接信息 ---
ipv4_ip_address = "//td[contains(text(), 'IP Address')]/following-sibling::td"
ipv4_connection_name = "//td[contains(text(), 'Connection Name')]/following-sibling::td"
ipv4_status = "//td[contains(text(), 'Status')]/following-sibling::td"
ipv4_gateway = "//td[contains(text(), 'Default Gateway')]/following-sibling::td"
ipv4_dns = "//td[contains(text(), 'DNS')]/following-sibling::td"


# ========================
# 🌐 Basic - WAN
# ========================
basic_wan_page = base_url + "/index.html#/basic/wan"
wan_enable_switch = "#wanEnable"
wan_connection_status = "#wanConnectionStatus"
wan_service_name_field = "#wanCurrentName input"
wan_service_name_option_INTERNET = 'li[id*="INTERNET"]'
wan_service_name_option_TR069 = 'li[id*="TR069"]'
wan_service_name_option_VOICE = 'li[id*="VOICE"]'
wan_work_mode_field = "#wanWorkMode input"
wan_work_mode_option_Route = 'li[id="Route"]'
wan_work_mode_option_Bridge = 'li[id="Bridge"]'
wan_bearer_service_field = "#wanService input"
wan_bearer_service_option_INTERNET = 'li[title*="INTERNET"]'
wan_bearer_service_option_IPTV = 'li[title*="IPTV"]'
wan_bearer_service_option_VOIP = 'li[title*="VOIP"]'
# Connection Mode (Route)
wan_conn_mode_field = "#wanConnectionMode input"
wan_conn_mode_option_DHCP = 'li[id="DHCP"]'
wan_conn_mode_option_Static = 'li[id="Static"]'
wan_conn_mode_option_PPPoE = 'li[id="PPPoE"]'
# Static IP
wan_ip_field = "#wanIpAddress input"
wan_netmask_field = "#wanIpMask input"
wan_gateway_field = "#wanGatewayIp input"
wan_dns1_field = "#wanFirstDns input"
wan_dns2_field = "#wanSecondDns input"
# PPPoE
wan_pppoe_username_field = "#wanPppoeUsername input"
wan_pppoe_password_field = "#wanPppoePassword input"
# VLAN
wan_vlan_mode_field = "#wanCurrentVlanMode input"
wan_vlan_mode_option_TAG = 'li[id="TAG"]'
wan_vlan_id_field = "#wanVlanId input"
wan_mtu_field = "#wanMtu input"
# IPv6
wan_ipv4_radio = 'label#IPv4 span.t-radio__input'
wan_ipv4_ipv6_radio = 'label#IPv4\\/IPv6 span.t-radio__input'
wan_ipv6_conn_mode_field = "#wanIpv6ConnectionMode input"
wan_ipv6_addr_field = "#wanIpV6Address input"
wan_ipv6_prefix_len_field = "#wanIpV6PrefixLe input"
wan_ipv6_gateway_field = "#wanIpv6Gateway input"
wan_ipv6_dns1_field = "#wanIpv6FirstDns input"
wan_save_button = "#wanSavelButton"

# ========================
# 🖥️ Basic - LAN
# ========================
basic_lan_page = base_url + "/index.html#/basic/lan"
lan_ipv4_addr_field = "#lanIpv4Address input"
lan_ipv4_netmask_field = "#lanIpv4Mask input"
lan_dhcp_enable_switch = "#dhcpEnable"
lan_dhcp_start_field = "#lanIpv4AddrStart input"
lan_dhcp_end_field = "#lanIpv4AddrEnd input"
lan_save_button = "#saveButton"
# IPv6
lan_ra_enable_switch = "#lanIpv6RadvdEnable"
lan_dhcpv6_enable_switch = "#lanIpv6DhcpEnable"
lan_ipv6_save_button = "#lanIpv6SaveButton"

# ========================
# ☁️ Basic - CWMP (TR-069)
# ========================
basic_cwmp_page = base_url + "/index.html#/basic/cwmp"
cwmp_enable_switch = "#cwmpPeriodEnable"
cwmp_interval_field = "#cwmpPeriodInterval input"
cwmp_acs_url_field = "#cwmpAcsUrl input"
cwmp_acs_username_field = "#cwmpAcsUserName input"
cwmp_acs_password_field = "#cwmpAcsPassWord input"
cwmp_client_username_field = "#cwmpClientReqUserName input"
cwmp_client_password_field = "#cwmpClientReqPassWord input"
cwmp_save_button = "#cwmpSaveButton"

# ========================
# 📞 Basic - VoIP
# ========================
basic_voip_page = base_url + "/index.html#/basic/voip"
voip_protocol_field = "#voipCurrentProtocol input"
voip_interface_field = "#voipCurrentInterface input"
voip_region_field = "#voipRegion input"
voip_reg_server_field = "#voipRegisterServer input"
voip_proxy_server_field = "#voipProxyServer input"
voip_proxy_port_field = "#voipProxyServerPort input"
voip_outbound_proxy_field = "#voipOutboundProxyServer input"
voip_outbound_port_field = "#voipOutboundProxyServerPort input"
voip_sec_reg_server_field = "#voipSecRegisterServer input"
voip_account_field = "#voipAccount"
voip_password_field = "#voipPassword"
voip_port_enable_switch = "#voipPortEnable"
voip_save_button = "#voipBasicSave"

# ========================
# 📺 Basic - IPTV
# ========================
basic_iptv_page = base_url + "/index.html#/basic/iptv"
iptv_enable_switch = "#multicastEnable"
iptv_lan1_bind_checkbox = '#LAN1 span.t-checkbox__input'
iptv_lan2_bind_checkbox = '#LAN2 span.t-checkbox__input'
iptv_lan3_bind_checkbox = '#LAN3 span.t-checkbox__input'
iptv_lan4_bind_checkbox = '#LAN4 span.t-checkbox__input'
iptv_access_mode_field = "#multicastMode input"
iptv_vlan_id_field = "#multicastVlanId input"
iptv_igmp_snooping_switch = "#igmpSnoopingEnable"
iptv_igmp_proxy_switch = "#igmpProxyEnable"
iptv_save_button = "#iptvSaveButton"

# ========================
# 📶 Basic - Wi-Fi 2.4G
# ========================
basic_wifi_24g_page = base_url + "/index.html#/basic/wifi/wifi24"
wifi_24g_enable_switch = "#bandSteeringEnable"
wifi_24g_ssid_field = "#wlanCurrentSsidName input"
wifi_24g_security_field = "#wlanCurrentEntrypt input"
wifi_24g_password_field = "#wlanPassword input"
wifi_24g_mode_field = "#wlanCurrentMode input"
wifi_24g_bandwidth_field = "#wlanCurrentBandwidth input"
wifi_24g_country_field = "#wlanCountry input"
wifi_24g_channel_field = "#wlanCurrentChannel input"
wifi_24g_signal_strength_field = "#wlanCurrentSignal input"
wifi_24g_save_button = "#wlanSave"

# ========================
# 📶 Basic - Wi-Fi 5G
# ========================
basic_wifi_5g_page = base_url + "/index.html#/basic/wifi/wifi5"
wifi_5g_enable_switch = "#bandSteeringEnable"
wifi_5g_ssid_field = "#wlan11acCurrentSsidName input"
wifi_5g_security_field = "#wlan11acCurrentEntrypt input"
wifi_5g_password_field = "#wlan11acPassword input"
wifi_5g_mode_field = "#wlan11acCurrentMode input"
wifi_5g_bandwidth_field = "#wlan11acCurrentBandwidth input"
wifi_5g_country_field = "#wlan11acCountry input"
wifi_5g_channel_field = "#wlan11acCurrentChannel input"
wifi_5g_signal_strength_field = "#wlan11acCurrentSignal input"
wifi_5g_save_button = "#wlan11acSave"

# ========================
# 🚪 Basic - Guest Wi-Fi
# ========================
basic_wifi_guest_page = base_url + "/index.html#/basic/wifi/guest"
guest_2g_enable_switch = "#guestWifi2GEnable"
guest_2g_ssid_field = "#guestWifi2GSsidName input"
guest_2g_password_field = "#guestWifi2GPassword input"
guest_2g_max_devices_field = "#guestWifi2GDeviceCount input"
guest_5g_enable_switch = "#guestWifi5GEnable"
guest_5g_ssid_field = "#guestWifi5GSsidName input"
guest_5g_password_field = "#guestWifi5GPassword input"
guest_5g_max_devices_field = "#guestWifi5GDeviceCount input"
guest_save_button = "#guestWifiSave"

# ========================
# 🔒 Basic - Parental Control
# ========================
basic_parental_control_page = base_url + "/index.html#/basic/parentalControl"
parental_control_enable_switch = "#parentalEnableStatus"
parental_add_rule_button = "#parentalAdd"
parental_mac_input = "#mac"
parental_add_mac_button = "#onAddMac"
parental_choose_device_button = "#onChooseDevice"
parental_time_active_switch = "#parentalCtlDurationActive"
parental_start_time_field = "#starttime0 input"
parental_end_time_field = "#endtime0 input"
parental_weekday_checkbox = "#week0 input"
parental_add_time_button = "#addTime"
parental_url_filter_switch = "#parentalCtlActiveUrl"
parental_list_type_black_radio = "#Black span.t-radio__input"
parental_list_type_white_radio = "#White span.t-radio__input"
parental_address0_field = "#addressItem0"
parental_cancel_button = "#cancel"
parental_save_button = "#save"

# ========================
# ⚙️ Basic - Operate Mode
# ========================
basic_operate_mode_page = base_url + "/index.html#/basic/mode"
mode_gpon_radio = "#modeGPON"
mode_epon_radio = "#modeEPON"

# ========================
# 📡 Basic - EasyMesh
# ========================
basic_easymesh_page = base_url + "/index.html#/basic/EasyMesh"
easymesh_enable_switch = "#meshEnable"
easymesh_version_field = "#meshVersion"
easymesh_role_field = "#meshRole input"
easymesh_steering_switch = "#steerEnable"
easymesh_reset_button = "#reset"
easymesh_trigger_button = "#meshTrigger"
easymesh_save_button = "#meshSaveButton"

# ========================
# 📊 Basic - Band Steering
# ========================
basic_bandsteer_page = base_url + "/index.html#/basic/wifi/bandsteer"
bandsteer_enable_switch = "#wifiband"
bandsteer_ssid_field = "#bnadSteeringSsid input"
bandsteer_security_field = "#bnadSteeringCurrentEntrypt input"
bandsteer_password_field = "#bnadSteeringPassword input"
bandsteer_2g_to_5g_rssi_field = "#bnadSteering2GTo5GRssi input"
bandsteer_5g_to_2g_rssi_field = "#bnadSteering5GTo2GRssi input"
bandsteer_save_button = "#bnadSteeringSave"

# ========================
# 👥 Basic - Access Devices
# ========================
basic_access_devices_page = base_url + "/index.html#/basic/device"
# 通常只读表格，无需操作元素

# ========================
# 🚀 Advanced - Speed Test
# ========================
advanced_speed_test_page = base_url + "/index.html#/advanced/network/speedTest"
speed_test_start_button = "#startTest"

# ========================
# 📦 Advanced - QoS
# ========================
advanced_qos_page = base_url + "/index.html#/advanced/network/qos"
qos_enable_switch = "#qosEnable"
qos_uplink_bw_field = "#qosUplinkBandwidth input"
qos_dscp_switch = "#qosDscp"
qos_8021p_switch = "#qosEn8021PRemark input"
qos_rule_type_disc_radio = '#discRule span.t-radio__input'
qos_rule_type_app_radio = '#appRule span.t-radio__input'
qos_scheduling_pq_radio = "#PQ span.t-radio__input"
qos_scheduling_wrr_radio = "#WRR span.t-radio__input"
qos_app_add_rule_button = "#appRuleAdd"

# ========================
# 🔗 Advanced - Port Binding
# ========================
advanced_port_binding_page = base_url + "/index.html#/advanced/network/binding"
# 页面内容为 FTP Client? 可能配置错误，暂不定义

# ========================
# 📁 Advanced - FTP Client
# ========================
advanced_ftp_client_page = base_url + "/index.html#/advanced/network/ftpClient"
ftp_usb_status = "#ftpClientUsbConnectStatus"
ftp_download_progress = "#ftpDownloadProgress"
ftp_download_url_field = "#ftpClientDownloadUrl input"
ftp_usb_interface_field = "#ftpClientUsbInterfaceName input"
ftp_auth_enable_switch = "#ftpClientAuthEnable"
ftp_username_field = "#ftpDownloadName input"
ftp_password_field = "#ftpDownloadPassword input"
ftp_save_button = "#ftpDownSaveButton"

# ========================
# 🔐 Advanced - Firewall
# ========================
advanced_firewall_page = base_url + "/index.html#/advanced/user/Firewall"
firewall_enable_switch = "#enablefire"
firewall_level_field = "#firewallLevel input"

# ========================
# 🛡️ Advanced - MAC Filter
# ========================
advanced_mac_filter_page = base_url + "/index.html#/advanced/user/macFilter"
mac_filter_enable_switch = "#macFilterEnable"
mac_filter_add_button = "#macFilterAddButton"
mac_filter_name_field = "#macFilterName input"
mac_filter_mac_field = "#macAddress input"
mac_filter_save_button = "button.t-dialog__confirm"

# ========================
# 🌐 Advanced - URL Filter
# ========================
advanced_url_filter_page = base_url + "/index.html#/advanced/user/urlFilter"
url_filter_enable_switch = "#urlFilterEnable"
url_filter_add_button = "#urlFilterAddButton"
url_filter_url_field = "#urlFilterUrl input"
url_filter_save_button = "button.t-dialog__confirm"

# ========================
# 🔒 Advanced - ACL
# ========================
advanced_acl_page = base_url + "/index.html#/advanced/user/aclFilter"
acl_enable_switch = "#aclEnable"
acl_add_button = "#aclAddButton"
acl_name_field = "#aclName input"
acl_src_ip_start_field = "#aclSrcIPStart input"
acl_src_ip_end_field = "#aclSrcIPEnd input"
acl_app_field = "#aclApplication input"
acl_interface_field = "#aclInterface input"
acl_save_button = "button.t-dialog__confirm"

# ========================
# 🔄 Advanced - Port Forward
# ========================
advanced_port_forward_page = base_url + "/index.html#/advanced/user/portForward"
port_forward_add_button = "#portForwardAddButton"
port_forward_app_field = "#curApplication input"
port_forward_protocol_field = "#portMappingProtocol input"
port_forward_ext_port_field = "#externalPort input"
port_forward_int_port_field = "#internalPort input"
port_forward_int_host_field = "#internalHost input"
port_forward_name_field = "#mappingName input"
port_forward_save_button = "#saveButton"

# ========================
# 💾 Advanced - System - Password
# ========================
advanced_password_page = base_url + "/index.html#/advanced/system/password"
password_username_field = "#loginUsername input"
password_new_field = "#newPassword input"
password_confirm_field = "#confirmPassword input"
password_save_button = "#saveButton"

# ========================
# 🔄 Advanced - System - Upgrade
# ========================
advanced_upgrade_page = base_url + "/index.html#/advanced/system/upgrade"
upgrade_file_input = ".t-upload input"
upgrade_commit_button = "#update"

# ========================
# ⏰ Advanced - System - Time Setting
# ========================
advanced_time_setting_page = base_url + "/index.html#/advanced/system/timeSetting"
time_auto_switch = "#automatic"
time_sntp1_field = "#timeSettingSntpServer1 input"
time_sntp2_field = "#timeSettingSntpServer2 input"
time_interval_field = "#timeSettingInterval input"
time_zone_field = "#timeSettingZone input"
time_save_button = "#timeSettingSaveButton"

# ========================
# 📝 Advanced - System - Log Manage
# ========================
advanced_log_manage_page = base_url + "/index.html#/advanced/system/logManage"
log_enable_switch = "#systemLogEnable"
log_level_field = "#systemLogLevel input"
log_download_button = "#downloadButton"

# ========================
# 🔁 Advanced - System - Timed Reboot
# ========================
advanced_timed_reboot_page = base_url + "/index.html#/advanced/system/autoReboot"
timed_reboot_enable_switch = "#autoRebootEnable"
timed_reboot_sun_checkbox = 'div.t-checkbox-group > label:nth-child(1) span.t-checkbox__input'
timed_reboot_mon_checkbox = 'div.t-checkbox-group > label:nth-child(2) span.t-checkbox__input'
timed_reboot_tue_checkbox = 'div.t-checkbox-group > label:nth-child(3) span.t-checkbox__input'
timed_reboot_wed_checkbox = 'div.t-checkbox-group > label:nth-child(4) span.t-checkbox__input'
timed_reboot_thu_checkbox = 'div.t-checkbox-group > label:nth-child(5) span.t-checkbox__input'
timed_reboot_fri_checkbox = 'div.t-checkbox-group > label:nth-child(6) span.t-checkbox__input'
timed_reboot_sat_checkbox = 'div.t-checkbox-group > label:nth-child(7) span.t-checkbox__input'
timed_reboot_time_field = "#autoRebootTime input"
timed_reboot_save_button = "#autoRebootSaveButton"

# ========================
# 🔌 Advanced - System - PON Auth
# ========================
advanced_pon_auth_page = base_url + "/index.html#/advanced/system/ponAuth"
pon_auth_mode_field = "#ponCurrentAuth input"
pon_loid_field = "#ponLoid input"
pon_loid_password_field = "#ponLoidPasswd input"
pon_password_field = "#ponPassword"
pon_auth_save_button = "#ponAuthSaveButton"

# ========================
# 🛠️ Advanced - System - Tool
# ========================
advanced_tool_page = base_url + "/index.html#/advanced/system/tool"
tool_telnet_enable_switch = "#telnetEnable"
tool_wan_mirror_enable_switch = "#wanMirrorEnable"

# ========================
# 🕵️ Hidden Page (Engineering Mode)
# ========================
hide_page = base_url + "/index.html#/hidePage"

# --- Common Settings ---
hide_common_setting_title = "div.t-collapse-panel__header:contains('Common Setting')"

# --- Upgrade Section ---
hide_upgrade_title = "div.t-collapse-panel__header:contains('Upgrade')"
hide_upgrade_file_input = "#upgradeFile input"  # 假设有文件上传
hide_upgrade_commit_button = "#upgradeCommit"

# --- Password Management ---
hide_password_mgmt_title = "div.t-collapse-panel__header:contains('Password Management')"
hide_password_username_field = "#hideUsername input"
hide_password_old_field = "#hideOldPassword input"
hide_password_new_field = "#hideNewPassword input"
hide_password_confirm_field = "#hideConfirmPassword input"
hide_password_save_button = "#hidePasswordSave"

# --- Device Management ---
hide_device_mgmt_title = "div.t-collapse-panel__header:contains('Device Management')"
hide_device_reboot_button = "#deviceReboot"
hide_device_factory_reset_button = "#factoryReset"

# --- Device Information ---
hide_device_info_title = "div.t-collapse-panel__header:contains('Device Information')"
hide_device_model = "#deviceModel"
hide_device_serial = "#deviceSerial"
hide_device_software_version = "#softwareVersion"
hide_device_hardware_version = "#hardwareVersion"

# --- Factory Management ---
hide_factory_mgmt_title = "div.t-collapse-panel__header:contains('Factory Management')"
hide_factory_restore_button = "#factoryRestore"

# --- Key Toggle Switches ---
hide_telnet_enable_switch = "#telnetEnable"
hide_wan_mirror_enable_switch = "#wanMirrorEnable"

# --- Login Form (if re-auth required) ---
hide_login_username_field = "#loginUsername input"
hide_login_password_field = "#loginPassword input"
hide_login_submit_button = "#loginCommit"
