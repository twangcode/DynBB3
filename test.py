import subprocess
import time

def get_ADR_factor(symbol):
	# run "findc" script from python to get factor symbol (dollar sign symbol)
	process_1 = subprocess.Popen(['findc', symbol], stdout=subprocess.PIPE)
	process_2 = subprocess.Popen(['grep', symbol], stdin=process_1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	out = process_2.communicate()[0]
	factor_symbol = out.split()[9]
	
	# run "snapshot" script to get factor
	factor = subprocess.check_output(['snapshot', factor_symbol, 'last']).split('=')[1]
	
	return factor

def test_run():
	start_time = time.time()
	for i in range(50):
		get_ADR_factor('ZN')
	run_time = time.time() - start_time
	print "run time is: ", run_time

if __name__ == "__main__":
	test_run()

