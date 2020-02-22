#!/usr/bin/env python3

import time

from hawkbit import HawkbitTestClient

def test_upgrade():

    hawkbit = HawkbitTestClient("localhost", "8080", username="admin", password="admin")

    filename_ptxdist = 'images/rpi-demo-bundle-raspberrypi3.raucb'
    filename_yocto = 'images/update.raucb'

    # Add expected targets
    hawkbit.add_target("RPI-1", "0815")
    hawkbit.add_target("RPI-2", "0815")
    hawkbit.add_target("RPI-3", "0815")
    hawkbit.add_target("RPI-4", "0815")
    hawkbit.add_target("RPI-5", "0815")
    hawkbit.add_target("RPI-6", "0815")

    # Create modules with artifacts
    module_id_a = hawkbit.add_swmodule('PTXdist module')
    module_id_b = hawkbit.add_swmodule('Yocto module')
    hawkbit.add_artifact(module_id_a, filename_ptxdist)
    hawkbit.add_artifact(module_id_b, filename_yocto)
    # Create distributions of it
    dist_id = [0,0]
    dist_id[0] = hawkbit.add_distributionset(module_id_a, name="Poky-Test")
    dist_id[1] = hawkbit.add_distributionset(module_id_b, name="PTXdist-Test1")

    current_dist_id = 0
    rollout_count = 0

    while True:

        rollout_id = hawkbit.add_rollout("Test Rollout #{}".format(rollout_count), dist_id[current_dist_id], 3)

        rollout_status = hawkbit.get_endpoint('rollouts/{}'.format(rollout_id))
        while not rollout_status['status'] == 'ready':
            time.sleep(1)
            rollout_status = hawkbit.get_endpoint('rollouts/{}'.format(rollout_id))

        hawkbit.start_rollout(rollout_id)

        rollout_status = hawkbit.get_endpoint('rollouts/{}'.format(rollout_id))
        while not rollout_status['status'] == 'finished':
            time.sleep(30)
            rollout_status = hawkbit.get_endpoint('rollouts/{}'.format(rollout_id))

        current_dist_id = 0 if current_dist_id == 1 else 1
        rollout_count += 1

def main():
    test_upgrade()

if __name__ == "__main__":
    main()
