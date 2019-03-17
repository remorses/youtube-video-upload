from setuptools import setup



with open('VERSION', 'r') as fh:
    version = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = [x for x in fh.read().split('\n') if x]

setup(name='youtube_video_upload',
      version=version,
      description='Youtube video uploader',
      long_description="check https://github.com/remorses/youtube-video-upload for more",
      long_description_content_type='text/markdown',
      url='https://github.com/remorses/youtube-video-upload',
      author='Tommaso De Rossi',
      author_email='beats.by.morse@gmail.com',
      license='MIT',
      packages=['youtube_video_upload'],
      install_requires=requirements,
      zip_safe=False
)
