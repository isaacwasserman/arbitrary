import pkg_resources
from packaging import version


def package_installed(requirement):
    try:
        split_requirement = requirement.split()
        package_name = split_requirement[0]
        if len(split_requirement) == 1:
            required_version = ""
            operator = ""
            if package_name[:4] == "git+":
                package_name = package_name.split("/")[-1].split(".")[0]
        else:
            operator = split_requirement[1]
            required_version = split_requirement[2]
        installed_version = pkg_resources.get_distribution(package_name).version
        match operator:
            case ">=":
                return version.parse(installed_version) >= version.parse(required_version)
            case ">":
                return version.parse(installed_version) > version.parse(required_version)
            case "==":
                return version.parse(installed_version) == version.parse(required_version)
            case "<":
                return version.parse(installed_version) < version.parse(required_version)
            case "<=":
                return version.parse(installed_version) <= version.parse(required_version)
            case "":
                return True
            case _:
                return False
    except pkg_resources.DistributionNotFound:
        return False
