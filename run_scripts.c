#include <stdio.h>
#include <stdarg.h>


/* slurm_* prints to stdout */
void slurm_debug(const char *fmt, ...) {
  va_list arg;

  printf("debug: ");
  va_start (arg, fmt);
  vprintf (fmt, arg);
  va_end (arg);
  printf("\n");
}
void slurm_error(const char *fmt, ...) {
  va_list arg;

  printf("error: ");
  va_start (arg, fmt);
  vprintf (fmt, arg);
  va_end (arg);
  printf("\n");
}
void slurm_info(const char *fmt, ...) {
  va_list arg;

  printf("info: ");
  va_start (arg, fmt);
  vprintf (fmt, arg);
  va_end (arg);
  printf("\n");
}
void slurm_verbose(const char *fmt, ...) {
  va_list arg;

  printf("verbose: ");
  va_start (arg, fmt);
  vprintf (fmt, arg);
  va_end (arg);
  printf("\n");
}

#include <slurm/spank.h>

/* empty stubs to make linker happy */
enum spank_context spank_context(void) {
	return S_CTX_SLURMD;
}
spank_err_t spank_getenv(spank_t spank, const char *var, char *buf, int len) {
	return ESPANK_ERROR;
}
spank_err_t spank_get_item(spank_t spank, spank_item_t item, ...) {
	return ESPANK_ERROR;
}
spank_err_t spank_option_register(spank_t spank, struct spank_option *opt) {
	return ESPANK_ERROR;
}
int spank_remote(spank_t spank) {
	return ESPANK_ERROR;
}
spank_err_t spank_setenv(spank_t spank, const char *var, const char *val, int overwrite) {
	return ESPANK_ERROR;
}
const char * spank_strerror(spank_err_t err) {
	return "spankerr";
}
spank_err_t spank_unsetenv(spank_t spank, const char *var) {
	return ESPANK_ERROR;
}



/* function we're testing with */
int slurm_spank_init(spank_t sp, int ac, char *av[]);

int main(int argc, char *argv[]) {
	spank_t sp = {0};
	int rc;
	argc--; argv++;
	rc = slurm_spank_init(sp, argc, argv);
	printf("init: %d\n", rc);

	return rc;
}



