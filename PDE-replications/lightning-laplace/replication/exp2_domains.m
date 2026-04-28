% Experiment 2: Lightning solver on multiple domains with corner singularities.
% Report: domain name, #corners, DoFs, maxerr (boundary), wall time.

addpath('../refs');
warning('off','all');

results = {};   % name, nw, N, M, maxerr, t

function [name, N, M, maxerr, t] = runone(name, P, g, tol)
   tic;
   if isempty(g)
      [u, maxerr, f, Z, Zplot, A] = laplace(P, 'noplots', 'tol', tol);
   else
      [u, maxerr, f, Z, Zplot, A] = laplace(P, g, 'noplots', 'tol', tol);
   end
   t = toc;
   N = size(A,2); M = size(A,1);
   fprintf('%-30s  N=%4d  M=%4d  maxerr=%8.2e  t=%6.3fs\n', ...
      name, N, M, maxerr, t);
end

tol = 1e-8;

% 1) L-shape
[n,N,M,e,t] = runone('L-shape (6 corners)', [2 2+1i 1+1i 1+2i 2i 0], [], tol);
results(end+1,:) = {n,N,M,e,t};

% 2) Isospectral drum (8 corners, standard Lightning test)
P = ([1+2i 1+3i 2i 1i+1 2+1i 2 3+1i 3+2i]-(1.5+1.5i))/1.8;
[n,N,M,e,t] = runone('Isospectral drum (8 corners)', P, [], tol);
results(end+1,:) = {n,N,M,e,t};

% 3) Snowflake with alternating BCs (discontinuous BC = crack-like singularity)
P = exp(2i*pi*(1:12)/12).*(1+.2*(-1).^(1:12))/1.4;
h = [0 0 1 1 0 0 1 1 0 0 1 1];
[n,N,M,e,t] = runone('Snowflake (12c, disc BC)', P, h, tol);
results(end+1,:) = {n,N,M,e,t};

% 4) Square with piecewise-constant BCs (harmonic meas.) — generates singular BC
P = [-1 1 1+1i -1+1i];
h = [0 0 1 0];
[n,N,M,e,t] = runone('Square disc BC (harmonic)', P, h, tol);
results(end+1,:) = {n,N,M,e,t};

% 5) "Crack" / slit approximation: thin rectangle 0.02 wide with a reentrant
% vertex giving near-360° reentrant angle (classic crack singularity).
% Model slit by a very narrow triangle jutting in -- approximates u ~ r^{1/2}.
eps = 0.01;
P = [-1-1i 1-1i 1+1i eps+eps*1i 0 eps-eps*1i 1+1i*eps 1+1i*(1-eps) ... 
     -1+1i];
% Simpler: pentagon with 270-degree reentrant corner = classic L-shape already.
% Use the "jigsaw" from examples.m -- reentrant + circular arcs
P2 = {2 [2+1i -1] 1+2i 2i [1.3i .3] .7i 0 [.7 -.3] 1.3};
[n,N,M,e,t] = runone('Jigsaw (circular arcs + reentrants)', P2, [], tol);
results(end+1,:) = {n,N,M,e,t};

% 6) Pentagon (convex, no corner sing., should be easy)
[n,N,M,e,t] = runone('Regular pentagon (convex)', 'pent', [], tol);
results(end+1,:) = {n,N,M,e,t};

% 7) 270-degree reentrant corner direct -- slit domain via L-like with near-360
% The strongest singularity the paper mentions is exterior angle 2*pi => r^{1/2}.
% Model via a near-slit pentagon.
slit = [0 1 1+1i -1+1i -1 -1e-3];
[n,N,M,e,t] = runone('Near-slit (crack-like)', slit, [], tol);
results(end+1,:) = {n,N,M,e,t};

% Save summary CSV
fid = fopen('exp2_domains.csv','w');
fprintf(fid,'domain,N_dofs,M_samples,maxerr,walltime_s\n');
for i = 1:size(results,1)
   fprintf(fid,'%s,%d,%d,%.3e,%.3f\n', results{i,1}, results{i,2}, results{i,3}, results{i,4}, results{i,5});
end
fclose(fid);
disp('Saved exp2_domains.csv');
