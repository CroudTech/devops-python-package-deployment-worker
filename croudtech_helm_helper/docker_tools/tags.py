import json
import semver


class Tags:
    def __init__(self, branch, tag=False, build=False, tag_master=False):
        self.branch = branch
        self.tag = tag
        self.build = build
        self.tag_master = tag_master

    def get_tags(self):
        tags = []
        if self.tag == None and self.branch == "master" and self.tag_master:
            tags.append("stable")
        if self.tag and semver.VersionInfo.isvalid(self.tag) and self.branch == 'master':
            ver = semver.VersionInfo.parse(self.tag)
            tags = [str(ver.major)]
            tags.append("stable")
            if ver.minor:
                tags.append("%s.%s" % (ver.major, ver.minor))
            if ver.patch:
                tags.append("%s.%s.%s" % (ver.major, ver.minor, ver.patch))
            if ver.build:
                tags.append("%s.%s.%s-%s" % (ver.major, ver.minor, ver.patch, ver.build))
            if self.build:
                tags.append(
                    "%s.%s.%s-%s" % (ver.major, ver.minor, ver.patch, self.build)
                )
        elif self.tag and self.branch != 'master':
            if self.build:
                tags.append(
                    "%s-%s-%s" % (self.branch.replace('/', '-'), self.tag, self.build)
                )
            else:
                tags.append(
                    "%s-%s" % (self.branch.replace('/', '-'), self.tag)
                )


        if self.branch == "integration":
            tags.append("integration")
            if self.build:
                tags.append("integration-%s" % self.build)
        return list(set(tags))

    def get_formatted_tags(self, format):
        if format == "json":
            return json.dumps(self.get_tags())
        if format == "plain":
            return "\n".join(self.get_tags())
