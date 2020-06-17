import json
import semver


class Tags:
    def __init__(self, branch, tag=False, build=False, tag_main=False, main_branch_name="main"):
        self.branch = branch
        self.tag = tag
        self.build = build
        self.tag_main = tag_main
        self.main_branch_name = main_branch_name

    def get_tags(self, single):
        if single:
            return self.get_single_tag()
        else:
            return self.get_multiple_tags()

    def get_single_tag(self):
        tag = 'latest'
        if self.tag == None and self.branch == self.main_branch_name and self.tag_main:
            tag = "stable"
        if self.tag and semver.VersionInfo.isvalid(self.tag) and self.branch == self.main_branch_name:
            tag = self.tag
        elif self.tag and self.branch != self.main_branch_name:
            if self.build:
                tag = "%s-%s-%s" % (self.branch.replace('/', '-'), self.tag, self.build)
            else:
                tag = "%s-%s" % (self.branch.replace('/', '-'), self.tag)

        if self.branch == "integration":
            tag = "integration"
            if self.build:
                tag = "integration-%s" % self.build
        return tag

    def get_multiple_tags(self):
        tags = []
        if self.tag == None and self.branch == self.main_branch_name and self.tag_main:
            tags.append("stable")
        if self.tag and semver.VersionInfo.isvalid(self.tag) and self.branch == self.main_branch_name:
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
        elif self.tag and self.branch != self.main_branch_name:
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

    def get_formatted_tags(self, format, single):
        if single:
            return str(self.get_tags(single))
        if format == "json":
            return json.dumps(self.get_tags(single))
        if format == "plain":
            return "\n".join(self.get_tags(single))

