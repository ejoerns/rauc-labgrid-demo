import pytest
import time

from labgrid.external import HawkbitTestClient
from labgrid.driver import InfoDriver

def test_hawkbit(hawkbit):
    """ xxx """
    pass

def test_upgrade(hawkbit):

    #info = gateway.get_driver(InfoDriver)
    filename = '/media/enrico/485d48ec-c44e-45b5-ba5c-52e362b1c6f7/YOCTO.BSP-PTX-RPI-Rauc-Demo/build/tmp/deploy/images/raspberrypi3/rpi-demo-bundle-raspberrypi3.raucb'
    # Manipulate hawkBit configuration
    # Add a target with the right name
    #hawkbit.add_target(info.get_hostname(), 'qwerty')
    #hawkbit.delete_target(info.get_hostname())
    # Create modules with artifacts
    module_id_a = hawkbit.add_swmodule('Yocto 0')
    module_id_b = hawkbit.add_swmodule('Yocto 1')
    hawkbit.add_artifact(module_id_a, filename)
    hawkbit.add_artifact(module_id_b, filename)
    # Create distributions of it
    dist_id = [0,0]
    dist_id[0] = hawkbit.add_distributionset(module_id_a, name="Poky-Test-0")
    dist_id[1] = hawkbit.add_distributionset(module_id_b, name="Poky-Test-1")

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

    # # Assign to all available targets
    # targets = hawkbit.get_endpoint('targets')['content']
    # for target in targets:
    #     target_id = target['controllerId']
    #     print ("Target ID: {}".format(target_id))
    #     foo = hawkbit.assign_target(dist_id_a, target_id)

    # # cleanup
    # hawkbit.delete_distributionset(dist_id_a)
    # hawkbit.delete_swmodule(module_id)
    # hawkbit.delete_artifact(module_id, artifact_id)

    #gw_shell.run_check("cp /etc/bcds-gateway-admin.hawkbit-client.ini /etc/bcds-gateway-admin.hawkbit-client.ini.test")
    #gw_shell.run_check("sed -i 's/hawkbit_server\=.*$/hawkbit_server={}/g' /etc/bcds-gateway-admin.hawkbit-client.ini.test".format('192.168.23.4:8080'))
    #gw_shell.run_check("sed -i 's/ssl\=.*$/ssl=false/g' /etc/bcds-gateway-admin.hawkbit-client.ini.test")
    #gw_shell.run_check("sed -i 's/auth_token\=.*$/auth_token=qwerty/g' /etc/bcds-gateway-admin.hawkbit-client.ini.test")
    #gw_shell.run_check("sed -i 's/tenant_id\=.*$/tenant_id=DEFAULT/g' /etc/bcds-gateway-admin.hawkbit-client.ini.test")
    #gw_shell.run_check("mount --bind /etc/bcds-gateway-admin.hawkbit-client.ini.test /etc/bcds-gateway-admin.hawkbit-client.ini")
    #gw_shell.run_check("systemctl restart --no-block bcds-gateway-admin.service")
    #gw_shell.wait_for("systemctl is-active bcds-gateway-admin", "active")
    #gw_shell.wait_for("journalctl --no-pager -u bcds-gateway-admin -n 10", "Sending identifying information to HawkBit")
