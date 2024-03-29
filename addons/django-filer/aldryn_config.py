from aldryn_client import forms


class Form(forms.BaseForm):

    def to_settings(self, data, settings):
        from functools import partial

        from aldryn_addons.utils import boolean_ish, djsenv
        from aldryn_django import storage
        from easy_thumbnails.conf import Settings as EasySettings

        EasyThumbnailSettings = EasySettings(isolated=True)
        env = partial(djsenv, settings=settings)

        # django-filer
        settings['FILER_ENABLE_PERMISSIONS'] = False
        settings['FILER_DEBUG'] = boolean_ish(env('FILER_DEBUG', settings['DEBUG']))
        settings['FILER_ENABLE_LOGGING'] = boolean_ish(env('FILER_ENABLE_LOGGING', True))
        settings['FILER_IMAGE_USE_ICON'] = True
        settings['ADDON_URLS'].append(
            'filer.server.urls'
        )
        settings.setdefault('MEDIA_HEADERS', []).insert(0, (
            r'filer_public(?:_thumbnails)?/.*',
            {
                'Cache-Control': 'public, max-age={}'.format(86400 * 365),
            },
        ))

        # easy-thumbnails
        settings['THUMBNAIL_QUALITY'] = env('THUMBNAIL_QUALITY', 90)
        settings['THUMBNAIL_PRESERVE_EXTENSIONS'] = ['png', 'gif']
        settings['THUMBNAIL_CACHE_DIMENSIONS'] = True

        # Swap scale and crop for django-filer version
        settings['THUMBNAIL_PROCESSORS'] = tuple([
            processor
            if processor != 'easy_thumbnails.processors.scale_and_crop'
            else 'filer.thumbnail_processors.scale_and_crop_with_subject_location'
            for processor in EasyThumbnailSettings.THUMBNAIL_PROCESSORS
        ])

        # easy_thumbnails uses django's default storage backend (local file
        # system storage) by default, even if the DEFAULT_FILE_STORAGE setting
        # points to something else.
        # If the DEFAULT_FILE_STORAGE has been set to a value known by
        # aldryn-django, then use that as THUMBNAIL_DEFAULT_STORAGE as well.
        for storage_backend in storage.SCHEMES.values():
            # Process before django 4.2
            if storage_backend == settings.get('DEFAULT_FILE_STORAGE', None):
                settings['THUMBNAIL_DEFAULT_STORAGE'] = storage_backend
                break
            # Process django 4.2 and after
            if storage_backend == settings.get('STORAGES', {}).get('default', {}).get('BACKEND', None):
                settings['THUMBNAIL_DEFAULT_STORAGE'] = storage_backend
                break
        return settings
