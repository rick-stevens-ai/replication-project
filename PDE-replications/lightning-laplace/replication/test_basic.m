% Basic test of laplace.m in Octave
addpath('../refs');

% Example from help: L-shape, known exact value u(0.99+0.99i) = 1.0267919261073...
disp('=== Test 1: L-shape, default BC g(z)=Re(z)^2, tol=1e-8 ===');
tic;
[u, maxerr, f, Z, Zplot, A] = laplace('L', 'noplots', 'tol', 1e-8);
t = toc;
uval = u(0.99 + 0.99i);
fprintf('u(0.99+0.99i) = %.15f\n', uval);
fprintf('expected      = 1.0267919261073...\n');
fprintf('maxerr        = %.3e\n', maxerr);
fprintf('wall time     = %.3f s\n', t);
fprintf('size(A)       = %d x %d\n', size(A,1), size(A,2));
