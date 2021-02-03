source_dir=""
target_dir=""

main() {

	[ -z ${SOURCE} ] && echo "SOURCE required but not set" && exit 1
	[ ! -d ${SOURCE} ] && "${SOURCE} does not exist" && exit 1

	[ -z ${TARGET} ] && echo "TARGET required but not set" && exit 1
	[ ! -d ${TARGET} ] && mkdir -p ${TARGET}

	source_dir=${SOURCE}
	target_dir=${TARGET}


	echo ${source_dir}
	echo ${target_dir}

		
	for result_dir in ${source_dir}/*; do
		if [ -d ${result_dir} ]; then
			result_dir_name=$(basename ${result_dir})
			mkdir -p "${target_dir}/${result_dir_name}"
			cp ${result_dir}/{solver-queries.kquery,all-queries.kquery,run.stats,info,instructions.txt,log.txt} "${target_dir}/${result_dir_name}"
		fi
	done
}

main $@
