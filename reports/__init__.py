from logidoor.libs.cores import actions


def makeReport(data, path):
	actions.file_write(path, data)