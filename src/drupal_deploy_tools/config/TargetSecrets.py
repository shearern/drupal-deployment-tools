

class TargetSecrets(object):
    '''Read secrets file for a deployment target'''

    # Bring in secrets
    secret_pat = re.compile(r'^([A-Z_]*)=(.*)$')
    info[self.instance_name]['secrets'] = dict()
    secret_path = find_secrets_file(self.instance_name)
    with open(secret_path, 'rt') as fh:
        for line in fh.readlines():
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            m = secret_pat.match(line)
            if not m:
                abort("Malformed line in %s: %s" % (secret_path, line))
            info[self.instance_name]['secrets'][m.group(1)] = m.group(2)
    for expected in ['SSH_USER', 'SSH_KEYFILE', 'DB_PASS', 'DB_USER']:
        if not info[self.instance_name]['secrets'].has_key(expected):
            abort("Secrets file %s is missing %s=" % (secret_path, expected))
