{
	'variables': {
		'media%': 1,
		'output%': '',
		'ar%': 'ar',
		'ranlib%': 'ranlib',
		'library%': 'static_library',
		'ff_install_dir':  '<(output)/obj.target/ffmpeg',
		'ff_product_path%': '<(ff_install_dir)/libffmpeg.a',
		'ff_openssl_gyp%': '../../deps/node/deps/openssl/openssl.gyp',
		'ff_zlib_gyp%': '../../deps/node/deps/zlib/zlib.gyp',
		'ff_build_sh%': '../../tools/build_ffmpeg.sh',
	},
	'targets': [
	{
		'target_name': 'ffmpeg_compile',
		'type': 'none',
		'actions': [{
			'action_name': 'ffmpeg_compile',
			'inputs': [ 'RELEASE', 'config.h' ],
			'outputs': [ '<(ff_product_path)' ],
			'conditions': [
				['media==1', {
					'action': [
						'<(ff_build_sh)',
						'<(bin)',
						'<(ff_install_dir)',
						'<(ff_product_path)',
						'<(ar)',
						'<(ranlib)',
					],
				}, {
					'action': ['echo', 'skip ffmpeg compile'],
				}]
			],
		}],
	},
	{
		'target_name': 'ffmpeg',
		'type': 'none',
		'direct_dependent_settings': {
			'include_dirs': [ '<(ff_install_dir)/include' ],
			'defines': [ '__STDC_CONSTANT_MACROS', ],
		},
		'dependencies': [
			# '<(ff_openssl_gyp):openssl',
			# '<(ff_zlib_gyp):zlib',
			'ffmpeg_compile',
		],
		'sources': [
			'libavutil/avutil.h',
			'libavformat/avformat.h',
			'libswresample/swresample.h',
			'libavcodec/avcodec.h',
		],
		'link_settings': {
			'libraries': [
				'<(ff_product_path)',
			]
		},
		'conditions': [
			['os in "ios osx"', {
				'link_settings': {
					'libraries': [
						'$(SDKROOT)/System/Library/Frameworks/AudioToolbox.framework',
						'$(SDKROOT)/System/Library/Frameworks/CoreVideo.framework',
						'$(SDKROOT)/System/Library/Frameworks/VideoToolbox.framework',
						'$(SDKROOT)/System/Library/Frameworks/CoreMedia.framework',
						'$(SDKROOT)/usr/lib/libiconv.tbd',
						'$(SDKROOT)/usr/lib/libbz2.tbd',
						'$(SDKROOT)/usr/lib/libz.tbd',
					],
				},
			}],
			['os=="android"', {
				'link_settings': {
					'libraries': [ '-lz' ],
				},
			}],
			['os=="linux"', {
				'link_settings': {
					'libraries': [ '-lbz2', '-lz' ],
				},
			}],
		],
	},
	],
}