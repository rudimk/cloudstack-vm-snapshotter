import os
import schedule
import time
from cs import CloudStack


def runSnapshotCycle():
	cs = CloudStack(endpoint=os.getenv('ACS_API'), key=os.getenv('ACS_KEY'), secret=os.getenv('ACS_SECRET'))
	# Grab a list of all VMs
	allVMs = cs.listVirtualMachines(listall=True)
	snapshotSources = []
	# Find IDs of VMs that have the snapshot=true KV pair, and add them to the snapshot source list
	for vm in allVMs['virtualmachine']:
		for tags in vm['tags']:
			if tags['key'] == 'snapshot' and tags['value'] == 'true':
				snapshotSources.append(vm['id'])
	# Now start making requests for creating VM snapshots for the VMs in the snapshot source list
	for source in snapshotSources:
		snapshot = cs.createVMSnapshot(virtualmachineid=source)
		print(f"Creating snapshot: {snapshot}")


# Schdule snapshot runs for 1AM daily
schedule.every().day.at("01:00").do(runSnapshotCycle)


if __name__ == '__main__':
	print("Initating cloudstack-vm-snapshotter...")
	schedule.run_pending()
	time.sleep(1)


