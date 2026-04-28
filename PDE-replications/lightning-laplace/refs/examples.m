% examples.m - explore laplace.m code - Nick Trefethen, November 2019

% Here are 27 examples to illustrate various Laplace solutions.
% For more info, see https://people.maths.ox.ac.uk/trefethen/lightning.html.

disp('Input an example number n from 1 to 30, or 0 to stop.')
disp('Examples 28 to 32 involve some homogeneous Neumann data.')

while 1

  disp(' ')
  n = input('n? ');
  if n == 0, break, end

  switch n

    case 1
    disp('L shape')
    P = [2 2+1i 1+1i 1+2i 2i 0];
    laplace(P);

    case 2
    disp('circular L shape')
    P = {2 [2+1i -1] 1+2i 2i 0};
    laplace(P);

    case 3
    disp('jigsaw puzzle')
    P = {2 [2+1i -1] 1+2i 2i [1.3i .3] .7i 0 [.7 -.3] 1.3};
    laplace(P);

    case 4
    disp('isospectral drum')
    P = ([1+2i 1+3i 2i 1i+1 2+1i 2 3+1i 3+2i]-(1.5+1.5i))/1.8;
    laplace(P);

    case 5
    disp('#2 again with ''slow'' to force equal # poles at all vertices')
    P = ([1+2i 1+3i 2i 1i+1 2+1i 2 3+1i 3+2i]-(1.5+1.5i))/1.8;
    laplace(P,'slow');

    case 6
    disp('curvy square')
    r = 1.7;
    P = {[0 -r] [1 -r] [1+1i -r] [1i -r]};
    laplace(P,[0 1 2 1]);

    case 7
    disp('example from Louis Howell 1994')
    P = {-2-2i [.4-2i -.5] 1.4-2i 2-2i 2+.8i [-.6+.8i -1.4] -2-.6i};
    laplace(P);

    case 8
    disp('rectangle with piecewise constant BCs')
    P = [-1 1 1+1i -1+1i];
    h = [0 0 1 0];
    laplace(P,h,'rel');

    case 9
    disp('same as #4 but to accuracy 1e-10')
    P = [-1 1 1+1i -1+1i];
    h = [0 0 1 0];
    laplace(P,h,'rel','tol',1e-10);

    case 10
    disp('rectangle with vertex added at point of BC singularity')
    P = [-1 0 1 1+1i -1+1i];
    h = @(z) abs(z);
    laplace(P,h);

    case 11
    disp('snowflake with alternating BCs')
    P = exp(2i*pi*(1:12)/12).*(1+.2*(-1).^(1:12))/1.4;
    h = [0 0 1 1 0 0 1 1 0 0 1 1];
    laplace(P,h,'rel');

    case 12
    disp('triangle with continuous BC')
    P = [0 1 -.5+1i]; 
    h = @(z) exp(real(z));
    laplace(P,h);

    case 13
    disp('equilateral triangle with one non-constant BC')
    h = {@(x) cos(pi*x/2), @(z) 0*z, @(z) 0*z};
    P = [-1 1 1i*sqrt(3)];
    laplace(P,h);

    case 14
    disp('random 10-gon, different each time')
    laplace(10);

    case 15
    disp('tilted 4x1 rectangle')
    P = sqrt(1i)*[0 4 4+1i 1i];
    h = [0 1 0 0];
    laplace(P,h,'rel');

    case 16
    disp('pentagon with linear boundary data')
    P = exp(pi*2i*(1:5)/5); 
    h = @(z) -real(z);
    laplace(P,h);

    case 17
    disp('pentagon with analytic boundary data')
    P = exp(pi*2i*(1:5)/5); 
    h = @(z) real(log(2-z));
    laplace(P,h);

    case 18
    disp('same but with singularity near boundary')
    P = exp(pi*2i*(1:5)/5); 
    h = @(z) real(log(1.01-z));
    laplace(P,h);

    case 19
    disp('dumbbell')
    P = 4+[1-2i 4-2i 4+2i 1+2i 1+1i -1+1i -1+2i -4+2i -4-2i -1-2i -1-1i 1-1i]; 
    laplace(P);

    case 20
    disp('reentrant spike with lowered tolerance')
    P = [0 1 1+.3i .5+.5i 1+.7i 1+1i 1i];
    laplace(P,'tol',1e-4);

    case 21
    disp('salient spike')
    P = [0 1 1+.3i 1.5+.5i 1+.7i 1+1i 1i];
    laplace(P);

    case 22
    disp('Fourier decay')
    P = [-pi/2 pi/2 pi/2+1i -pi/2+1i];
    h = {@(x) sin(4*x), @(z) 0*z, @(z) 0*z, @(z) 0*z};
    laplace(P,h);

    case 23
    disp('narrow neck -- note extra vertex added to aid convergence')
    P = [-4 0 4 4+1i .5i -4+1i];
    laplace(P);

    case 24
    disp('U shape (two extra vertices to aid convergence)')
    P = [-1+1i -1-.5i -1-1i 1-1i 1-.5i 1+.5i 0.8+.5i 0.8-.5i -.8-.5i -.8+1i]; 
    h = @(z) abs(z);
    laplace(P,h);

    case 25
    disp('wedding cake')
    P = [4 4+1i 3+1i 3+2i 2+2i 2+3i 1+3i 1+4i ...
         -1+4i -1+3i -2+3i -2+2i -3+2i -3+1i -4+1i -4];
    h = @(z) abs(z-5i);
    laplace(P,h);

    case 26
    disp('diamond with log data')
    P = [1 .5i -1 -.5i];
    h = @(z) -log(abs(z));
    laplace(P,h,'tol',1e-10,'rel');

    case 27
    disp('pinched diamond with log data')
    z = .3*exp(.25i*pi);
    P = [1 z 1i 1i*z -1 -z -1i -1i*z];
    h = @(z) -log(abs(z));
    laplace(P,h,'tol',1e-10,'rel');

    case 28
    disp('L shape with some Neumann sides')
    P = [2 2+1i 1+1i 1+2i 2i 0];
    h = [nan 0 0 nan 1 1];
    laplace(P,h);

    case 29
    disp('circular L shape with some Neumann sides')
    P = {2 [2+1i -1] 1+2i 2i 0};
    h = [nan 0 nan 1 1];
    laplace(P,h);

    case 30
    disp('U shape with Neumann data')
    P = [-1+.3i -1-1i 1-1i 1+.5i 0.5+.5i 0.5-.5i -.5-.5i -.5+.3i]; 
    h = [0 0 0 nan 1 1 1 nan];
    laplace(P,h);

    case 31
    disp('isospectral drum with Dirichlet/Neumann sides')
    P = ([1+2i 1+3i 2i 1i+1 2+1i 2 3+1i 3+2i]-(1.5+1.5i))/1.8;
    h = [0 nan 1 1 1 nan 0 0];
    laplace(P,h);

    case 32 
    disp('random hexagone with some Neumann sides')
    h = [nan 1 1 nan 0 0];
    laplace(6,h);

    otherwise
    h = @(z) abs(z);
    nv = randi(8)+2;
    if randn<.4
        disp('Out of range.  Here''s a random polygon for you.')
        laplace(nv,h);
    else
        disp('Out of range.  Here''s a random circular polygon for you.')
        laplace(-nv,h);
    end 
  end

end
