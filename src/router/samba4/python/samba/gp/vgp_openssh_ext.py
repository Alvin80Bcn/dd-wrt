# vgp_openssh_ext samba group policy
# Copyright (C) David Mulder <dmulder@suse.com> 2020
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from io import BytesIO
from samba.gp.gpclass import gp_xml_ext, gp_file_applier
from tempfile import NamedTemporaryFile
from samba.common import get_bytes, get_string

intro = b'''
### autogenerated by samba
#
# This file is generated by the vgp_openssh_ext Group Policy
# Client Side Extension. To modify the contents of this file,
# modify the appropriate Group Policy objects which apply
# to this machine. DO NOT MODIFY THIS FILE DIRECTLY.
#

'''

class vgp_openssh_ext(gp_xml_ext, gp_file_applier):
    def __str__(self):
        return 'VGP/Unix Settings/OpenSSH'

    def process_group_policy(self, deleted_gpo_list, changed_gpo_list,
            cfg_dir='/etc/ssh/sshd_config.d'):
        for guid, settings in deleted_gpo_list:
            if str(self) in settings:
                for attribute, sshd_config in settings[str(self)].items():
                    self.unapply(guid, attribute, sshd_config)

        for gpo in changed_gpo_list:
            if gpo.file_sys_path:
                xml = 'MACHINE/VGP/VTLA/SshCfg/SshD/manifest.xml'
                path = os.path.join(gpo.file_sys_path, xml)
                xml_conf = self.parse(path)
                if not xml_conf:
                    continue
                policy = xml_conf.find('policysetting')
                data = policy.find('data')
                configfile = data.find('configfile')
                for configsection in configfile.findall('configsection'):
                    if configsection.find('sectionname').text:
                        continue
                    settings = {}
                    for kv in configsection.findall('keyvaluepair'):
                        settings[kv.find('key')] = kv.find('value')
                    raw = BytesIO()
                    for k, v in settings.items():
                        raw.write(b'%s %s\n' % \
                                  (get_bytes(k.text), get_bytes(v.text)))
                    # Each GPO applies only one set of OpenSSH settings, in a
                    # single file, so the attribute does not need uniqueness.
                    attribute = self.generate_attribute(gpo.name)
                    # The value hash is generated from the raw data we will
                    # write to the OpenSSH settings file, ensuring any changes
                    # to this GPO will cause the file to be rewritten.
                    value_hash = self.generate_value_hash(raw.getvalue())
                    if not os.path.isdir(cfg_dir):
                        os.mkdir(cfg_dir, 0o640)
                    def applier_func(cfg_dir, raw):
                        f = NamedTemporaryFile(prefix='gp_',
                                               delete=False,
                                               dir=cfg_dir)
                        f.write(intro)
                        f.write(raw.getvalue())
                        os.chmod(f.name, 0o640)
                        filename = f.name
                        f.close()
                        return [filename]
                    self.apply(gpo.name, attribute, value_hash, applier_func,
                               cfg_dir, raw)
                    raw.close()

    def rsop(self, gpo):
        output = {}
        if gpo.file_sys_path:
            xml = 'MACHINE/VGP/VTLA/SshCfg/SshD/manifest.xml'
            path = os.path.join(gpo.file_sys_path, xml)
            xml_conf = self.parse(path)
            if not xml_conf:
                return output
            policy = xml_conf.find('policysetting')
            data = policy.find('data')
            configfile = data.find('configfile')
            for configsection in configfile.findall('configsection'):
                if configsection.find('sectionname').text:
                    continue
                for kv in configsection.findall('keyvaluepair'):
                    if str(self) not in output.keys():
                        output[str(self)] = {}
                    output[str(self)][kv.find('key').text] = \
                        kv.find('value').text
        return output
