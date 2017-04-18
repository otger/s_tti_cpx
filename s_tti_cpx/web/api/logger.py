import logging

log = logging.getLogger('entropyfw.modules.tti_cpx.api')
log.setLevel(logging.DEBUG)

nh = logging.NullHandler()
log.addHandler(nh)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
