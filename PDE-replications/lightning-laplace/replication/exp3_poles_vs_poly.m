% Experiment 3: Poles + polynomial (Lightning) vs polynomial-only (no poles) on L-shape.
% Reproduces the paper's core claim: corner poles enable root-exp convergence,
% pure polynomials stagnate at a low accuracy due to r^{2/3} singularity at reentrant corner.

addpath('../refs');
warning('off','all');

% We use 'slow' option to force equal #poles at every corner.
% We also instrument laplace.m lightly: the quickest way is to sweep 'tol'
% and log (N, maxerr) pairs.  But for polynomial-only we hack by passing
% no corners -- easier: use a smooth convex domain (pentagon) where poly works
% and compare.
% Better: use the 'steps' internal but that needs interactive.

% Strategy: run laplace with 'slow' and multiple tolerances to get a cleaner
% convergence curve.  Record maxerr and N.  These are "Lightning (poles+poly)".
tols = 10.^(-[2 3 4 5 6 7 8 9 10]);
lightning = zeros(length(tols), 3);
for i = 1:length(tols)
   tic;
   [u, maxerr, f, Z, Zplot, A] = laplace('L', 'noplots', 'slow', 'tol', tols(i));
   t = toc;
   lightning(i,:) = [size(A,2), maxerr, t];
   fprintf('Lightning(slow)  tol=%.0e N=%4d maxerr=%.2e t=%.2fs\n', tols(i), size(A,2), maxerr, t);
end

% Polynomial-only: patch laplace.m to skip pole addition.  Quickest: make
% a minimal reimplementation here.  We compute error with polynomial-only
% Arnoldi-stabilized basis for increasing degree n on the L-shape.

disp(' ');
disp('=== Polynomial-only basis on L-shape (no clustered poles) ===');

% L-shape
w = [2 2+1i 1+1i 1+2i 2i 0].';
nw = length(w);
for k = 1:nw
   kn = mod(k,nw)+1;
   dw(k) = abs(w(kn)-w(k));
   pt{k} = @(t) w(k) + t*(w(kn)-w(k))/dw(k);
end
ww = w([1:end 1]);
wc = mean(w);
scl = max([max(real(w))-min(real(w)), max(imag(w))-min(imag(w))]);
g = @(z) real(z).^2;

% Many sample points on boundary, densely near corners, so geometry is well-resolved
M_per_side = 300;
Z = [];
for k = 1:nw
   s = linspace(1e-10, 1-1e-10, M_per_side).';
   % Chebyshev-like clustering toward endpoints (near corners)
   s = (1 - cos(pi*s))/2;
   Z = [Z; pt{k}(s*dw(k))];
end
G = real(Z).^2;

poly_res = [];
for n = [4 8 16 24 32 48 64 96 128 192]
   % Arnoldi-stabilized basis on Z
   Mz = length(Z);
   H = zeros(n+1,n);
   Q = ones(Mz,1);
   for k = 1:n
      v = (Z-wc).*Q(:,k);
      for j = 1:k
         H(j,k) = Q(:,j)'*v/Mz;
         v = v - H(j,k)*Q(:,j);
      end
      H(k+1,k) = norm(v)/sqrt(Mz);
      Q = [Q v/H(k+1,k)];
   end
   A = [real(Q) imag(Q(:,2:n+1))];
   c = A \ G;
   err = norm(A*c - G, inf);
   poly_res = [poly_res; n, 2*n+1, err];
   fprintf('Polynomial only   n=%3d N=%4d maxerr=%.2e\n', n, 2*n+1, err);
end

% Save both
fid = fopen('exp3_lightning.csv','w');
fprintf(fid,'tol,N,maxerr,walltime\n');
for i = 1:size(lightning,1)
   fprintf(fid,'%.1e,%d,%.6e,%.4f\n', tols(i), lightning(i,1), lightning(i,2), lightning(i,3));
end
fclose(fid);

fid = fopen('exp3_polynomial.csv','w');
fprintf(fid,'n,N,maxerr\n');
for i = 1:size(poly_res,1)
   fprintf(fid,'%d,%d,%.6e\n', poly_res(i,1), poly_res(i,2), poly_res(i,3));
end
fclose(fid);
disp('Saved exp3_lightning.csv and exp3_polynomial.csv');
