{
	'variables': {
		'media%': 1,
		'output%': '',
		'ar%': 'ar',
		'ranlib%': 'ranlib',
		'library%': 'static_library',
		'ff_install_dir':  '<(output)/obj.target/FFmpeg',
		'ff_product_path%': '<(ff_install_dir)/libFFmpeg.a',
		'ff_openssl_gyp%': '../../depe/node/deps/openssl/openssl.gyp',
		'ff_zlib_gyp%': '../../depe/node/deps/zlib/zlib.gyp',
		'ff_build_sh%': '../../tools/build_FFmpeg.sh',
	},
	'targets': [
	{
		'target_name': 'FFmpeg_compile',
		'type': 'none',
		'actions': [{
			'action_name': 'FFmpeg_compile',
			'inputs': [ 'RELEASE', 'config.h' ],
			'outputs': [ '<(ff_product_path)' ],
			'conditions': [
				['media==1', {
					'action': [ 'sh', '-c', 
						'export PATH=<(tools):<(bin):\"${PATH}\";'
						'export INSTALL_DIR=<(ff_install_dir);'
						'export PRODUCT_PATH=<(ff_product_path);'
						'export AR=<(ar);'
						'export RANLIB=<(ranlib);'
						'sh <(ff_build_sh)'
					],
				}, {
					'action': ['echo', 'skip FFmpeg compile'],
				}]
			],
		}],
	},
	{
		'target_name': 'FFmpeg',
		'type': 'none',
		'direct_dependent_settings': {
			'include_dirs': [ '<(ff_install_dir)/include' ],
			'defines': [ '__STDC_CONSTANT_MACROS', ],
		},
		'dependencies': [
			# '<(ff_openssl_gyp):openssl',
			# '<(ff_zlib_gyp):zlib',
			'FFmpeg_compile',
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