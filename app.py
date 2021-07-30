import os
from cs import CloudStack
import arrow


cs = CloudStack(endpoint=os.getenv('ACS_API'), key=os.getenv('ACS_KEY'), secret=os.getenv('ACS_SECRET'))

def runSnapshotCycle():

	# Delete snapshots older than 3 days
	deleteSnaps(3)

	# Grab a list of all resources with the 'snapshot' tag in them.
	# allTags = cs.listTags(listall=True, key='snapshot')
	allTags = cs.listTags(key='snapshot')
	snapshotSources = []

	if allTags:
		for resource in allTags['tag']:
			snapshotSources.append(resource['resourceid'])

		# Now start making requests for creating VM snapshots for the VMs in the snapshot source list
		for source in snapshotSources:
			snapshot = cs.createVMSnapshot(virtualmachineid=source)
			print(f"Creating snapshot: {snapshot}")



def deleteSnaps(ndays):

	# allsnaps = cs.listVMSnapshot(listall=True)
	allSnaps = cs.listVMSnapshot()
	utc = arrow.now('IST')

	if allSnaps:

		for resource in allSnaps['vmSnapshot']:
			snapDate = arrow.get(resource['created']).humanize(utc)
			print(snapDate)

			if snapDate == f'{ndays} days ago':
				snapId = resource['id']
				responce = cs.deleteVMSnapshot(vmsnapshotid=snapId)
				print(responce)



if __name__ == '__main__':
	print("Initating cloudstack-vm-snapshotter...")
	runSnapshotCycle()

