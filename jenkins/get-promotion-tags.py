#!/usr/bin/python -tt
#
# (c) Copyright 2016 Hewlett Packard Enterprise Development Company LP
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


"""
Used in Jenkins promotion jobs to get tags from jobs.yml and
   then call sort_artifacts to place artifacts in the correct
    location on the staging server.

This requires the JOB_NAME, PROMOTED_JOB_NAME and JENKINS_URL
   environment variables from Jenkins.
"""

import argparse
import os
import urllib2
import yaml

JOBS_CONFIG_FILENAME = 'jobs.yml'


def get_promoted_job_name():
    return os.getenv('PROMOTED_JOB_NAME')


def get_promotion_name():
    return os.getenv('JOB_NAME').rsplit('/', 1)[-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-j', '--job', default=os.getenv('JOB_NAME'))
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('--jenkins-url',
                        default=os.getenv('JENKINS_URL'))
    args = parser.parse_args()
    if not args.job:
        parser.error('argument -j/--job or JOB_NAME is required')
    if not args.jenkins_url:
        parser.error('argument --jenkins-url or JENKINS_URL is required')

    url = '{url}/userContent/{tag_map}'.format(url=args.jenkins_url,
                                               tag_map=JOBS_CONFIG_FILENAME)
    promotion = get_promotion_name()
    jobname = get_promoted_job_name()
    job_config = yaml.safe_load(urllib2.urlopen(url).read())
    tags = job_config.get('jobs').get(jobname, {}).get('promotion-tags', {}).get(promotion, [])
    print "{sep}".format(sep=' '.join(tags))



if __name__ == '__main__':
    main()
