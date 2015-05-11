#!/usr/bin/python
#
# Copyright 2015 Derek Marcotte
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for GlanceURLProvider class"""

import re
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["GlanceURLProvider"]


GLANCE_DOWNLOAD_URL = "http://www.glance.net/install/install.asp"
RE_GLANCE_ZIP = re.compile(
	r'href="(?P<url>/install/GlanceMac_[^"]+\.zip)"', re.I)


class GlanceURLProvider(Processor):
	"""Provides URL to the latest binary release of Glance."""
	description = __doc__
	input_variables = {
		"download_url": {
			"required": False,
			"description": "Default is '" + GLANCE_DOWNLOAD_URL + "'.",
		},
	}
	output_variables = {
		"url": {
			"description": "URL to the latest binary release of Glance.",
		},
	}

	def get_glance_zip_url(self, download_url):
		"""Find download URL for zip download"""
		#pylint: disable=no-self-use
		# Read HTML index.
		try:
			# Without specifing an Accept, the server returns
			# Content-Location: unarchiver.css instead of unarchiver.html
			req = urllib2.Request(download_url)
			fref = urllib2.urlopen(req)
			html = fref.read()
			fref.close()
		except BaseException as err:
			raise ProcessorError("Can't download %s: %s" % (download_url, err))

		# Search for download link.
		match = RE_GLANCE_ZIP.search(html)
		if not match:
			raise ProcessorError(
				"Couldn't find Glance download URL in %s" % download_url)

		# Return URL.
		return match.group("url")

	def main(self):
		# Determine base_url.
		download_url = self.env.get('download_url', GLANCE_DOWNLOAD_URL)

		self.env["url"] = "http://www.glance.net" + self.get_glance_zip_url(download_url)
		self.output("Found URL %s" % self.env["url"])


if __name__ == '__main__':
	PROCESSOR = GlanceURLProvider()
	PROCESSOR.execute_shell()
