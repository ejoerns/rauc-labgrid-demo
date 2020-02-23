#!/usr/bin/env python3

import time
import coloredlogs, logging

from hawkbit import HawkbitTestClient
from hawkbit import HawkbitError

def test_upgrade():

    hawkbit = HawkbitTestClient("localhost", "8080", username="admin", password="admin")

    filename_ptxdist = 'images/rpi-demo-bundle-raspberrypi3.raucb'
    filename_yocto = 'images/update.raucb'

    # Add expected targets
    try:
        hawkbit.add_target("RPI-1", "0815")
        hawkbit.add_target("RPI-2", "0815")
        hawkbit.add_target("RPI-3", "0815")
        hawkbit.add_target("RPI-4", "0815")
        hawkbit.add_target("RPI-5", "0815")
        hawkbit.add_target("RPI-6", "0815")
    except HawkbitError as e:
        logging.warning("Adding targets failed: {}".format(e.json['message']))

    #hawkbit.add_target("test-target", "0815")

    dist_id = [0,0]
    try:
        # Create modules with artifacts
        module_id_a = hawkbit.add_swmodule('PTXdist module')
        module_id_b = hawkbit.add_swmodule('Yocto module')
        hawkbit.add_artifact(module_id_a, filename_ptxdist)
        hawkbit.add_artifact(module_id_b, filename_yocto)

        # Create distributions of it
        dist_id[0] = hawkbit.add_distributionset(module_id_a, name="Poky-Test")
        dist_id[1] = hawkbit.add_distributionset(module_id_b, name="PTXdist-Test1")
    except HawkbitError as e:
        logging.warning("Adding modules/artifacts/distributions failed: {}".format(e.json['message']))

        dist_id[0] = hawkbit.get_distribution_id("Poky-Test")
        if not dist_id[0]:
            raise Exception("Unable to find distriution 'Poky-Test'")
        dist_id[1] = hawkbit.get_distribution_id("PTXdist-Test1")
        if not dist_id[1]:
            raise Exception("Unable to find distriution 'PTXdist-Test1'")
        logging.info("Got IDs of existing distributions")

    current_dist_id = 0
    rollout_count = 0
    rollout_id = 0

    while True:

        try:
            rollout_id = hawkbit.add_rollout("Test Rollout #{}".format(rollout_count), dist_id[current_dist_id], 3)
            logging.info("Started rollout: #{}".format(rollout_id))
        except HawkbitError as e:
            logging.warning("Adding rollout failed: {}".format(e.json['message']))

            try:
                rollouts = hawkbit.get_endpoint('rollouts')
                current_rollout = rollouts['content'][-1]
                rollout_id = current_rollout['id']
                logging.info("Got current rollout id: {}".format(rollout_id))
            except:
                raise Exception("Failed getting current rollout")

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
    coloredlogs.install()
    try:
        test_upgrade()
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()
