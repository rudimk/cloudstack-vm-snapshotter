import os
from cs import CloudStack


def runSnapshotCycle():
	cs = CloudStack(endpoint=os.getenv('ACS_API'), key=os.getenv('ACS_KEY'), secret=os.getenv('ACS_SECRET'))
	# Grab a list of all resources with the 'snapshot' tag in them.
	allTags = cs.listTags(listall=True, key='snapshot')
	snapshotSources = []
	# Find IDs of VMs that have the snapshot=true KV pair, and add them to the snapshot source list
	for resource in allTags['tag']:
		snapshotSources.append(resource['resourceid'])
	# Now start making requests for creating VM snapshots for the VMs in the snapshot source list
	for source in snapshotSources:
		snapshot = cs.createVMSnapshot(virtualmachineid=source)
		print(f"Creating snapshot: {snapshot}")



if __name__ == '__main__':
	print("Initating cloudstack-vm-snapshotter...")
	runSnapshotCycle()


