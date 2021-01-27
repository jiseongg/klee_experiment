benchmark_base=""
result_dir=""
script_dir=""
bcfile=""
output_dir=""
run_in_dir=""

set_output_dir() {
	output_dir="${result_base}/$1-$2-$3-$4"
}

set_bcfile() {
	pgm=$1
	bcfile=$(find ${benchmark_base} -name "${pgm}.bc" 2>/dev/null)
}

set_script_dir() {
	script_base=$(cd "$(dirname $1)"; echo "${PWD}")
}

set_result_dir() {
	result_base="${script_base}/klee-results"
}

generate_sandbox() {

	if [[ ! -d "${script_base}/sandbox" ]]; then
		tar xvf "${script_base}/sandbox.tar" -C "${script_base}" > /dev/null
	fi
	run_in_dir="${script_base}/sandbox"
}

run_klee() {
	local pgm=$1
	local solver
	local max_time
	local searcher_name
	local searcher

	if [[ $# -eq 5 ]]; then
		solver=$4
		max_time=$5
		searcher_name="$2-$3"
		searcher="--search=$2 --search=$3"
	elif [[ $# -eq 4 ]]; then
		solver=$3
		max_time=$4
		searcher_name=$2
		searcher="--search=$2"
	else
		echo "Invalid arguments"
		exit
	fi

	set_output_dir ${pgm} ${searcher_name} ${solver} ${max_time}
	set_bcfile ${pgm}

	local solving_opt="--solver-backend=${solver} --ignore-solver-failures --simplify-sym-indices --use-forked-solver --use-query-log=all:kquery,solver:kquery"
	local debug_opt="--debug-print-instructions=all:file"
	local external_call_opt="--external-call=concrete"
	local linking_opt="--libc=uclibc --posix-runtime"
	local module_opt="--output-module --output-source --switch-type=internal --disable-inlining"
	local search_opt="${searcher} --use-batching-search --batch-instructions=10000"
	local startup_opt="--optimize"
	local termination_opt="--max-memory=4000 --max-memory-inhibit --max-time=${max_time} --watchdog --run-in-dir=${run_in_dir} --output-dir=${output_dir}"
	local statistics_opt="--output-istats --output-stats"
	local test_gen_opt="--dump-states-on-halt --emit-all-errors --only-output-states-covering-new"

	local args="--sym-args 0 1 10 --sym-args 0 2 2 --sym-files 1 8 --sym-stdin 8 --sym-stdout"
	
	generate_sandbox
	echo "KLEE running for ${pgm}"
	ulimit -s unlimited && ulimit -n 1000000 && ulimit -c unlimited && \
		klee \
		${solving_opt} ${debug_opt} ${externall_call_opt} \
		${linking_opt} ${module_opt} ${search_opt} ${startup_opt} \
		${termination_opt} ${statistics_opt} ${test_gen_opt} \
		${bcfile} ${args} > "${script_base}/log.txt" 2>&1
	echo "KLEE finished for ${pgm}"
	rm -rf "${script_base}/sandbox"
	mv "${script_base}/log.txt" "${output_dir}"
}

main() {
	set_script_dir $0
	set_result_dir
	if [[ -z "${BASE}" ]]; then
		echo "BASE Required but not set"
		exit 1
	fi
	benchmark_base=$BASE

	if [[ ! -d ${result_base} ]]; then
		mkdir -p "${result_base}"
	fi
	
	run_klee gcal dfs random-state stp 7200s
	run_klee combine dfs random-state stp 7200s
#	run_klee trueprint dfs random-state stp 7200s
}

main
