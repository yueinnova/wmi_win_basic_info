#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8
import wmi 
import sys,time,platform 
 
def get_system_info(os, wmiObj): 
	"""  
	获取操作系统版本。  
	"""  
	print 
	print "Operating system:" 
	if os == "Windows": 
		for sys in wmiObj.Win32_OperatingSystem(): 
			print '\t' + "Version :\t%s" % sys.Caption.encode("GBK") 
			print '\t' + "Vernum :\t%s" % sys.BuildNumber 
			print '\t' + "Arch :\t%s" % sys.OSArchitecture 

def get_memory_info(os, wmiObj): 
	"""  
	获取物理内存和虚拟内存。  
	"""  
	print 
	print "memory_info:" 
	if os == "Windows": 
		cs = wmiObj.Win32_ComputerSystem()  
		pfu = wmiObj.Win32_PageFileUsage()  
		MemTotal = int(cs[0].TotalPhysicalMemory)/1024/1024 
		print '\t' + "TotalPhysicalMemory :" + '\t' + str(MemTotal) + "M" 
		#tmpdict["MemFree"] = int(os[0].FreePhysicalMemory)/1024  
		SwapTotal = int(pfu[0].AllocatedBaseSize) 
		print '\t' + "SwapTotal :" + '\t' + str(SwapTotal) + "M" 
		#tmpdict["SwapFree"] = int(pfu[0].AllocatedBaseSize - pfu[0].CurrentUsage) 
 
def get_disk_info(os, wmiObj):  
	"""  
	获取物理磁盘信息。  
	"""  
	print 
	print "disk_info:" 
	if os == "Windows": 
		tmplist = []  
		for physical_disk in wmiObj.Win32_DiskDrive(): 
			# if physical_disk.Size: 
			print ('\t' + str(physical_disk.Caption) + 
				' :\t' + str(long(physical_disk.Size)/1024/1024/1024) + "G")
		for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"): 
			for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"): 
				print '\t', partition.Caption.encode("GBK"), logical_disk.Caption.encode('GBK'), '\t', str(long(logical_disk.Size)/1024/1024/1024) + "G"             
 
def get_cpu_info(os, wmiObj):  
	"""  
	获取CPU信息。  
	"""  
	print 
	print "cpu_info:" 
	if os == "Windows": 
		tmpdict = {}  
		tmpdict["CpuCores"] = 0  
		for cpu in wmiObj.Win32_Processor():             
			tmpdict["CpuType"] = cpu.Name  
		try:  
			tmpdict["CpuCores"] = cpu.NumberOfCores  
		except:  
			tmpdict["CpuCores"] += 1  
			tmpdict["CpuClock"] = cpu.MaxClockSpeed     
		print '\t' + 'CpuType :\t' + str(tmpdict["CpuType"]) 
		print '\t' + 'CpuCores :\t' + str(tmpdict["CpuCores"]) 
	"""
	获取内存动态使用率
	"""
		# t = 0
		# while t < 10:
		# 	for cpu in wmiObj.Win32_Processor(): 
		# 		timestamp = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()) 
		# 	 	print '%s | Utilization: %s: %d %%' % (timestamp, cpu.DeviceID, cpu.LoadPercentage) 
		# 	 	time.sleep(1)
		# 	 	t = t + 1
 
def get_network_info(os, wmiObj):  
	"""  
	获取网卡信息和当前TCP连接数。  
	"""  
	print 
	print "network_info:" 
	if os == "Windows": 
		tmplist = []  
		for interface in wmiObj.Win32_NetworkAdapterConfiguration (IPEnabled=1):  
				tmpdict = {}  
				tmpdict["Description"] = interface.Description  
				tmpdict["IPAddress"] = interface.IPAddress[0]  
				tmpdict["IPSubnet"] = interface.IPSubnet[0]  
				tmpdict["MAC"] = interface.MACAddress 
				tmplist.append(tmpdict)  
		for i in tmplist: 
			print '\t' + i["Description"] 
			print '\t' + '\t' + "MAC :" + '\t' + i["MAC"] 
			print '\t' + '\t' + "IPAddress :" + '\t' + i["IPAddress"] 
			print '\t' + '\t' + "IPSubnet :" + '\t' + i["IPSubnet"] 
		for interfacePerfTCP in wmiObj.Win32_PerfRawData_Tcpip_TCPv4():  
				print '\t' + 'TCP Connect :\t' + str(interfacePerfTCP.ConnectionsEstablished)  

def get_soft_info(os, wmiObj):  
	"""  
	获取应用列表。  
	"""  
	print 
	print "soft_info:" 
	if os == "Windows": 
		tmplist = []  
		for installed_software in wmiObj.Win32_Product(): 
			print '\t' + installed_software.Caption.encode('GBK') + '\t' + installed_software.Version.encode('GBK')

def get_process_info(os, wmiObj):
	"""  
	获取进程列表。  
	"""  
	print 
	print "process_info:"
	if os == "Windows":
		for process in wmiObj.Win32_Process(): 
			print '\t', process.ProcessId, '\t', process.Name 
 
if __name__ == "__main__": 
	os = platform.system() 
	# wmiObj = wmi.WMI (computer="192.168.56.102", user="Administrator", password="Admin123") 
	wmiObj = wmi.WMI ()
	get_system_info(os, wmiObj) 
	get_memory_info(os, wmiObj) 
	get_disk_info(os, wmiObj) 
	get_cpu_info(os, wmiObj) 
	get_network_info(os, wmiObj)
	get_process_info(os, wmiObj)
	get_soft_info(os, wmiObj)