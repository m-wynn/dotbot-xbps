import os, subprocess, dotbot
from enum import Enum

class PkgStatus(Enum):
    UP_TO_DATE = 'Up to date'
    INSTALLED = 'Installed'
    NOT_FOUND = 'Not found'
    ERROR = 'Errors occurred'
    NOT_SURE = 'Could not determine'

class XBPS(dotbot.Plugin):
    _directive = 'xbps'

    def __init__(self, context):
        super(XBPS, self).__init__(self)
        self._context = context
        self._strings = {}
        self._strings[PkgStatus.UP_TO_DATE] = 'already installed'
        self._strings[PkgStatus.INSTALLED] = 'installed'
        self._strings[PkgStatus.NOT_FOUND] = 'Unable to locate'

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if not self.can_handle(directive):
            raise ValueError('XBPS cannot handle directive %s' % directive)
        return self._process(data)

    def _process(self, packages):
        results = {}
        successful = [PkgStatus.UP_TO_DATE, PkgStatus.INSTALLED]

        for pkg in packages:
            process_result = self._install(pkg)
            results[process_result] = results.get(process_result, 0) + 1
            if process_result not in successful:
                self._log.error('Could not install package {}'.format(pkg))

        if all([result in successful for result in results.keys()]):
            self._log.info('All packages installed successfully')
            success = True
        else:
            success = False

        for status, amount in results.items():
            log = self._log.info if status in successful else self._log.error
            log('{} {}'.format(amount, status.value))

        return success

    def _install(self, pkg):
        cmd = 'xbps-install -Sy {}'.format(pkg)
        with_sudo = ""

        if os.getuid() != 0:
            cmd = 'sudo ' + cmd
            with_sudo = "with sudo"


        self._log.info('Installing \'{}\' {}'.format(pkg, with_sudo))

        process = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        out = process.stdout.read()
        process.stdout.close()

        for item in self._strings.keys():
            if out.find(self._strings[item]) >= 0:
                return item

        self._log.warn(
            "Could not determine what happened wth package {}".format(pkg))
        return PkgStatus.NOT_SURE
