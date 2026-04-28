% Experiment 1: L-shape convergence vs. number of DoFs.
% Paper (Gopal & Trefethen 2019) claims root-exp convergence err ~ exp(-c*sqrt(N))
% and ~10^-8 error with O(100) poles.  We reproduce the convergence curve.

addpath('../refs');
warning('off','all');

% Reference: classical Motz/L-shape corner problem.  With default BC g = Re(z)^2,
% and L-shape vertices [2 2+1i 1+1i 1+2i 2i 0], the help claims
% u(0.99+0.99i) = 1.0267919261073... (from NA Digest Nov 2018).
uref = 1.02679192610731;   % ~13-digit reference
probe = 0.99 + 0.99i;

tols = 10.^(-[2 3 4 5 6 7 8 9 10 11 12]);
results = zeros(length(tols), 6);
for i = 1:length(tols)
    tol = tols(i);
    tic;
    [u, maxerr, f, Z, Zplot, A] = laplace('L', 'noplots', 'tol', tol);
    tw = toc;
    uval = u(probe);
    err_point = abs(uval - uref);
    N = size(A,2);
    M = size(A,1);
    results(i,:) = [tol, N, M, maxerr, err_point, tw];
    fprintf('tol=%7.0e  N=%4d  M=%4d  maxerr=%8.2e  |u-uref|=%8.2e  t=%6.3fs\n', ...
        tol, N, M, maxerr, err_point, tw);
end

% Save CSV: tol, N (dofs), M (sample pts), maxerr, pointwise error, wall time
fid = fopen('exp1_Lshape_convergence.csv','w');
fprintf(fid,'tol,N_dofs,M_samples,maxerr,err_probe,walltime_s\n');
for i = 1:size(results,1)
    fprintf(fid,'%.2e,%d,%d,%.6e,%.6e,%.6f\n', ...
        results(i,1), results(i,2), results(i,3), ...
        results(i,4), results(i,5), results(i,6));
end
fclose(fid);

disp('Saved exp1_Lshape_convergence.csv');
