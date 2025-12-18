# element_config.py
# 完整支持所有页面 + Wi-Fi 2.4G / 5G 配置项

ELEMENT_CONFIG = {
    # ======================
    # 全局 URL 映射（哈希路由）
    # ======================
    "url_home": "/",
    "url_basic_wan": "#/basic/wan",
    "url_basic_lan": "#/basic/lan",
    "url_basic_cwmp": "#/basic/cwmp",
    "url_basic_voip": "#/basic/voip",
    "url_basic_iptv": "#/basic/iptv",
    "url_basic_wifi": "#/basic/wifi",
    "url_basic_wifi_2g": "#/basic/wifi/2.4G",  # 新增
    "url_basic_wifi_5g": "#/basic/wifi/5G",    # 新增
    "url_basic_guest_wifi": "#/basic/guest_wifi",
    "url_basic_access_devices": "#/basic/access_devices",
    "url_basic_parental_control": "#/basic/parentalControl",
    "url_basic_link_mode": "#/basic/mode",
    "url_basic_easymesh": "#/basic/easymesh",
    "url_advanced_qos": "#/advanced/qos",
    "url_advanced_static_route": "#/advanced/static_route",
    "url_advanced_ddns": "#/advanced/ddns",
    "url_advanced_port_forward": "#/advanced/port_forward",
    "url_advanced_mac_filter": "#/advanced/mac_filter",
    "url_advanced_url_filter": "#/advanced/url_filter",
    "url_advanced_acl_filter": "#/advanced/acl_filter",
    "url_advanced_dmz": "#/advanced/dmz",
    "url_advanced_algs": "#/advanced/algs",
    "url_advanced_upnp": "#/advanced/upnp",
    "url_advanced_samba": "#/advanced/samba",
    "url_advanced_vpn_ipsec": "#/advanced/vpn_ipsec",
    "url_advanced_vpn_l2tp": "#/advanced/vpn_l2tp",
    "url_advanced_system_password": "#/advanced/system/password",
    "url_advanced_system_upgrade": "#/advanced/system/upgrade",
    "url_advanced_system_time": "#/advanced/system/time",
    "url_advanced_system_device": "#/advanced/system/device",
    "url_advanced_system_led": "#/advanced/system/led",
    "url_advanced_system_loopback": "#/advanced/system/loopback",
    "url_advanced_system_test": "#/advanced/system/test",
    "url_advanced_system_tool": "#/advanced/system/tool",
    "url_hidepage": "/hidepage",

    # ======================
    # Basic - WAN
    # ======================
    "basic_wan_enable": "#enable",
    "basic_wan_request_name": "#requestName",
    "basic_wan_request_name_options": [
        "1_INTERNET_R_VID_100",
        "2_INTERNET_R_VID_200",
        "3_VOIP_R_VID_300",
        "4_IPTV_R_VID_400",
        "5_TR069_R_VID_500"
    ],
    "basic_wan_add_button": "#addButton",
    "basic_wan_access_type": "#accessType",
    "basic_wan_access_type_options": ["Route", "Bridge"],
    "basic_wan_bearer_service": "#bearerService",
    "basic_wan_bearer_service_options": ["INTERNET", "VOIP", "IPTV", "TR069"],
    "basic_wan_connection_mode": "#connectionMode",
    "basic_wan_connection_mode_options": ["PPPoE", "DHCP", "Static IP"],
    "basic_wan_vlan_gateway_type": "#vlanGatewayType",
    "basic_wan_vlan_gateway_type_options": ["Default Gateway", "User Defined"],
    "basic_wan_vlan_id": "#vlanId",
    "basic_wan_mtu": "#mtu",
    "basic_wan_nat_enable": "#natEnable",
    "basic_wan_bind_option_lan1": "#bindOptionLAN1",
    "basic_wan_bind_option_lan2": "#bindOptionLAN2",
    "basic_wan_bind_option_lan3": "#bindOptionLAN3",
    "basic_wan_bind_option_lan4": "#bindOptionLAN4",
    "basic_wan_protocol_version_ipv4": "#protocolVersionIPv4",
    "basic_wan_protocol_version_ipv6": "#protocolVersionIPv6",
    "basic_wan_delete_button": "#deleteButton",
    "basic_wan_save_button": "#saveButton",

    # ======================
    # Basic - LAN
    # ======================
    "basic_lan_ip": "#lanIp",
    "basic_lan_subnet_mask": "#subnetMask",
    "basic_lan_dhcp_server": "#dhcpServer",
    "basic_lan_ip_start": "#ipStart",
    "basic_lan_ip_end": "#ipEnd",
    "basic_lan_lease_time": "#leaseTime",
    "basic_lan_ra_mode": "#raMode",
    "basic_lan_ra_mode_options": ["Stateless", "Stateful", "Disabled"],
    "basic_lan_prefix_source": "#prefixSource",
    "basic_lan_prefix_source_options": ["Auto", "Manual"],
    "basic_lan_dhcpv6_server": "#dhcpv6Server",
    "basic_lan_dhcpv6_server_options": ["Stateless", "Stateful", "Disabled"],
    "basic_lan_configuration_mode": "#configurationMode",
    "basic_lan_configuration_mode_options": ["SLAAC", "DHCPv6", "Both"],
    "basic_lan_dns_source": "#dnsSource",
    "basic_lan_dns_source_options": ["Auto", "Manual"],
    "basic_lan_save": "#saveButton",

    # ======================
    # Basic - CWMP
    # ======================
    "basic_cwmp_periodic_notify": "#periodicNotificationEnable",
    "basic_cwmp_notify_interval": "#notificationInterval",
    "basic_cwmp_server_url": "#serverUrl",
    "basic_cwmp_platform_username": "#platformUsername",
    "basic_cwmp_platform_password": "#platformPassword",
    "basic_cwmp_terminal_username": "#terminalUsername",
    "basic_cwmp_terminal_password": "#terminalPassword",
    "basic_cwmp_save": "#saveButton",

    # ======================
    # Basic - VoIP
    # ======================
    "basic_voip_account": "#account",
    "basic_voip_password": "#password",
    "basic_voip_register_server": "#registerServer",
    "basic_voip_proxy_server": "#proxyServer",
    "basic_voip_save": "#saveButton",

    # ======================
    # Basic - IPTV
    # ======================
    "basic_iptv_enable": "#enable",
    "basic_iptv_multicast_vlan_id": "#multicastVlanId",
    "basic_iptv_igmp_snooping": "#igmpSnooping",
    "basic_iptv_igmp_proxy": "#igmpProxy",
    "basic_iptv_save": "#saveButton",

    # ======================
    # Basic - WiFi - 2.4G
    # ======================
    "basic_wifi_2g_enable": "#enable",
    "basic_wifi_2g_ssid": "#ssid",
    "basic_wifi_2g_encryption": "#encryption",
    "basic_wifi_2g_encryption_options": ["WEP", "WPA-PSK", "WPA2-PSK", "WPA3-PSK"],
    "basic_wifi_2g_wep_length": "#wepLength",
    "basic_wifi_2g_wep_length_options": ["64-bit", "128-bit"],
    "basic_wifi_2g_wep_key": "#wifi\\.wlanWepKey",
    "basic_wifi_2g_select_mode": "#selectMode",
    "basic_wifi_2g_select_mode_options": ["802.11b/g", "802.11n", "802.11ac"],
    "basic_wifi_2g_bandwidth": "#bandwidth",
    "basic_wifi_2g_bandwidth_options": ["20MHz", "40MHz"],
    "basic_wifi_2g_country": "#country",
    "basic_wifi_2g_country_options": ["RUSSIA", "USA", "CHINA", "JAPAN", "EUROPE"],
    "basic_wifi_2g_wireless_channel": "#wirelessChannel",
    "basic_wifi_2g_wireless_channel_options": ["Auto", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"],
    "basic_wifi_2g_signal_strength": "#signalStrength",
    "basic_wifi_2g_signal_strength_options": ["Low", "Medium", "High"],
    "basic_wifi_2g_save": "#saveButton",

    # ======================
    # Basic - WiFi - 5G
    # ======================
    "basic_wifi_5g_enable": "#enable",
    "basic_wifi_5g_ssid": "#ssid",
    "basic_wifi_5g_encryption": "#encryption",
    "basic_wifi_5g_encryption_options": ["WEP", "WPA-PSK", "WPA2-PSK", "WPA3-PSK"],
    "basic_wifi_5g_wep_length": "#wepLength",
    "basic_wifi_5g_wep_length_options": ["64-bit", "128-bit"],
    "basic_wifi_5g_wep_key": "#wifi\\.wlanWepKey",
    "basic_wifi_5g_select_mode": "#selectMode",
    "basic_wifi_5g_select_mode_options": ["802.11a", "802.11n", "802.11ac"],
    "basic_wifi_5g_bandwidth": "#bandwidth",
    "basic_wifi_5g_bandwidth_options": ["20MHz", "40MHz", "80MHz"],
    "basic_wifi_5g_country": "#country",
    "basic_wifi_5g_country_options": ["RUSSIA", "USA", "CHINA", "JAPAN", "EUROPE"],
    "basic_wifi_5g_wireless_channel": "#wirelessChannel",
    "basic_wifi_5g_wireless_channel_options": ["Auto", "36", "40", "44", "48", "52", "56", "60", "64", "100", "104", "108", "112", "116", "120", "124", "128", "132", "136", "140", "144", "149", "153", "157", "161", "165"],
    "basic_wifi_5g_signal_strength": "#signalStrength",
    "basic_wifi_5g_signal_strength_options": ["Low", "Medium", "High"],
    "basic_wifi_5g_save": "#saveButton",

    # ======================
    # Basic - Guest WiFi
    # ======================
    "basic_guest_2g_enable": "#guest2GEnable",
    "basic_guest_5g_enable": "#guest5GEnable",
    "basic_guest_ssid_2g": "#guestSSID2G",
    "basic_guest_ssid_5g": "#guestSSID5G",
    "basic_guest_password_2g": "#guestPassword2G",
    "basic_guest_password_5g": "#guestPassword5G",
    "basic_guest_expire_time": "#expireTime",
    "basic_guest_save": "#saveButton",

    # ======================
    # Basic - Access Devices
    # ======================
    "access_devices_online_count": "//div[contains(text(), 'Online Device(')]",
    "access_devices_offline_count": "//div[contains(text(), 'Offline Device(')]",
    "access_devices_first_device_name": "//tr[1]//td[contains(@class, 'device-name')]",
    "access_devices_first_device_ip": "//tr[1]//td[contains(text(), 'IP Address:')]",
    "access_devices_first_device_mac": "//tr[1]//td[contains(text(), 'MAC:')]",
    "access_devices_url_limit_btn": "//button[contains(text(), 'URL Limit')]",

    # ======================
    # Basic - Parental Control
    # ======================
    "basic_parental_control_enable": "#enable",
    "basic_parental_control_time_rule": "#timeRule",
    "basic_parental_control_website_list": "#websiteList",
    "basic_parental_control_add_website": "//button[contains(text(), 'Add')]",
    "basic_parental_control_save": "#saveButton",

    # ======================
    # Basic - Link Mode
    # ======================
    "basic_link_mode_enable": "#enable",
    "basic_link_mode_mode": "#mode",
    "basic_link_mode_mode_options": ["Bridge", "Router", "Repeater"],
    "basic_link_mode_save": "#saveButton",

    # ======================
    # Basic - EasyMesh
    # ======================
    "basic_easymesh_enable": "#enable",
    "basic_easymesh_network_name": "#networkName",
    "basic_easymesh_password": "#password",
    "basic_easymesh_save": "#saveButton",

    # ======================
    # Advanced - QoS
    # ======================
    "advanced_qos_enable": "#enableQos",
    "advanced_qos_uplink_bandwidth": "#uplinkBandwidth",
    "advanced_qos_downlink_bandwidth": "#downlinkBandwidth",
    "advanced_qos_save": "#saveButton",

    # ======================
    # Advanced - Static Route
    # ======================
    "advanced_static_route_add": "//button[contains(text(), 'Add')]",
    "advanced_static_route_ip_address": "#ipAddress",
    "advanced_static_route_gateway": "#gateway",
    "advanced_static_route_subnet_mask": "#subnetMask",
    "advanced_static_route_interface": "#interface",
    "advanced_static_route_interface_options": ["WAN1", "WAN2", "LAN"],
    "advanced_static_route_save": "//button[contains(text(), 'Confirm')]",

    # ======================
    # Advanced - DDNS
    # ======================
    "advanced_ddns_add": "//button[contains(text(), 'Add')]",
    "advanced_ddns_provider": "#provider",
    "advanced_ddns_provider_options": ["DynDNS", "No-IP", "DuckDNS", "Custom"],
    "advanced_ddns_host": "#host",
    "advanced_ddns_domain": "#domain",
    "advanced_ddns_username": "#username",
    "advanced_ddns_password": "#password",
    "advanced_ddns_enable": "#enable",
    "advanced_ddns_save": "#saveButton",

    # ======================
    # Advanced - Port Forward
    # ======================
    "advanced_port_forward_add": "//button[contains(text(), 'Add')]",
    "advanced_port_forward_protocol": "#protocol",
    "advanced_port_forward_protocol_options": ["TCP", "UDP", "Both"],
    "advanced_port_forward_external_port": "#externalPort",
    "advanced_port_forward_internal_port": "#internalPort",
    "advanced_port_forward_internal_host": "#internalHost",
    "advanced_port_forward_mapping_name": "#mappingName",
    "advanced_port_forward_application": "#application",
    "advanced_port_forward_application_options": ["HTTP", "HTTPS", "FTP", "SSH", "Custom"],
    "advanced_port_forward_save": "//button[contains(text(), 'Save')]",

    # ======================
    # Advanced - MAC Filter
    # ======================
    "advanced_mac_filter_add": "//button[contains(text(), 'Add')]",
    "advanced_mac_filter_devicename": "#devicename",
    "advanced_mac_filter_mac": "#mac",
    "advanced_mac_filter_save": "#saveButton",

    # ======================
    # Advanced - URL Filter
    # ======================
    "advanced_url_filter_input": "#urlFilterInput",
    "advanced_url_filter_add": "//button[contains(text(), 'Add')]",
    "advanced_url_filter_save": "#saveButton",

    # ======================
    # Advanced - DMZ
    # ======================
    "advanced_dmz_enable": "#enable",
    "advanced_dmz_host_ip": "#dmzHostIp",
    "advanced_dmz_save": "#saveButton",

    # ======================
    # Advanced - ALG
    # ======================
    "advanced_alg_l2tp": "#enableL2TPAlg",
    "advanced_alg_ipsec": "#enableIPSecAlg",
    "advanced_alg_h323": "#enableH323Alg",
    "advanced_alg_rtsp": "#enableRTSPAlg",
    "advanced_alg_sip": "#enableSIPAlg",
    "advanced_alg_ftp": "#enableFTPAlg",
    "advanced_alg_pptp": "#enablePPTPAlg",
    "advanced_alg_save": "#saveButton",

    # ======================
    # Advanced - System - Password
    # ======================
    "advanced_system_password_username": "#username",
    "advanced_system_password_new": "#newPassword",
    "advanced_system_password_confirm": "#confirmPassword",
    "advanced_system_password_save": "#saveButton",

    # ======================
    # Advanced - System - Upgrade
    # ======================
    "advanced_system_upgrade_file_input": "#file",
    "advanced_system_upgrade_button": "//button[contains(text(), 'Upgrade')]",

    # ======================
    # Advanced - System - Time
    # ======================
    "advanced_system_time_timezone": "#timeZone",
    "advanced_system_time_timezone_options": [
        "(GMT-12:00) International Date Line West",
        "(GMT-11:00) Midway Island, Samoa",
        "(GMT-10:00) Hawaii",
        "(GMT-09:00) Alaska",
        "(GMT-08:00) Pacific Time (US & Canada)",
        "(GMT-07:00) Mountain Time (US & Canada)",
        "(GMT-06:00) Central Time (US & Canada)",
        "(GMT-05:00) Eastern Time (US & Canada)",
        "(GMT-04:00) Atlantic Time (Canada)",
        "(GMT-03:00) Brasilia",
        "(GMT-02:00) Mid-Atlantic",
        "(GMT-01:00) Azores",
        "(GMT+00:00) London, Dublin, Lisbon",
        "(GMT+01:00) Paris, Berlin, Rome",
        "(GMT+02:00) Athens, Istanbul, Cairo",
        "(GMT+03:00) Moscow, Riyadh",
        "(GMT+04:00) Abu Dhabi, Muscat",
        "(GMT+05:00) Islamabad, Karachi",
        "(GMT+05:30) Chennai, Mumbai, New Delhi",
        "(GMT+06:00) Dhaka",
        "(GMT+07:00) Bangkok, Hanoi",
        "(GMT+08:00) Beijing, Chongqing, Hong Kong",
        "(GMT+09:00) Tokyo, Seoul",
        "(GMT+10:00) Sydney, Melbourne",
        "(GMT+11:00) Solomon Is.",
        "(GMT+12:00) Auckland, Wellington"
    ],
    "advanced_system_time_ntp_primary": "#masterSntpServer",
    "advanced_system_time_ntp_secondary": "#slaveSntpServer",
    "advanced_system_time_save": "#saveButton",

    # ======================
    # Advanced - System - Device Management
    # ======================
    "advanced_system_device_rom_file_input": "#file",
    "advanced_system_device_import_file": "//button[contains(text(), 'Import File')]",
    "advanced_system_device_rom_backup": "//button[contains(text(), 'ROM Backup')]",
    "advanced_system_device_restart": "//button[contains(text(), 'Restart')]",
    "advanced_system_device_reset_standard": "//button[contains(text(), 'Reset Standart')]",
    "advanced_system_device_reset_all": "//button[contains(text(), 'Reset All')]",

    # ======================
    # Advanced - System - LED
    # ======================
    "advanced_system_led_enable": "#ledEnable",
    "advanced_system_led_save": "#saveButton",

    # ======================
    # Advanced - System - Loop Back
    # ======================
    "advanced_system_loopback_enable": "#enable",
    "advanced_system_loopback_interval": "#sendingInterval",
    "advanced_system_loopback_port_close_time": "#portCloseTime",
    "advanced_system_loopback_ethernet_type": "#ethernetType",
    "advanced_system_loopback_ethernet_type_options": ["Unicast", "Multicast"],
    "advanced_system_loopback_vlan_tag": "#vlanTag",
    "advanced_system_loopback_vlan": "#vlan",
    "advanced_system_loopback_save": "#saveButton",

    # ======================
    # Advanced - System - Test
    # ======================
    "advanced_system_test_ping_repeat": "#repeatTimes",
    "advanced_system_test_ping_interface": "#pingInterface",
    "advanced_system_test_ping_interface_options": ["WAN", "LAN"],
    "advanced_system_test_ping_address": "#pingAddress",
    "advanced_system_test_ping_start": "//button[contains(text(), 'Start') and not(contains(@style, 'display: none'))][1]",
    "advanced_system_test_tracert_interface": "#tracertInterface",
    "advanced_system_test_tracert_interface_options": ["WAN", "LAN"],
    "advanced_system_test_tracert_address": "#tracertAddress",
    "advanced_system_test_tracert_start": "//button[contains(text(), 'Start') and not(contains(@style, 'display: none'))][2]",
    "advanced_system_test_inform_manual": "//button[contains(text(), 'Manual report')]",

    # ======================
    # Advanced - System - Tool
    # ======================
    "advanced_system_tool_telnet_enable": "#telnetEnable",
    "advanced_system_tool_wan_mirror_enable": "#wanMirrorEnable",
    "advanced_system_tool_save": "#saveButton",

    # ======================
    # Login
    # ======================
    "login_username": "input[placeholder='Please Enter Your Username']",
    "login_password": "input[placeholder='Please Enter Your Password']",
    "login_submit": "button[type='submit']",

    # ======================
    # Hide Page
    # ======================
    "hidepage_username": "input[name='Username']",
    "hidepage_password": "input[name='Password']",
    "hidepage_login": "input[value='Login']",
}