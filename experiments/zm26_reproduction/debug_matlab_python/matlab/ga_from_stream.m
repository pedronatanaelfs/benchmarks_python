function [Offspring, OffspringPreClip] = ga_from_stream(Parent, Lower, Upper, ...
        mu_sbx, sign01, beta_skip, proc, site_u, mu_mut, proC, disC, proM, disM)
%GA_FROM_STREAM  Diagnostic wrapper of Public/GA.m real encoding.
%
% Uses caller-supplied random arrays instead of rand/randi.
% Does NOT modify production GA.m.
%
% Random arrays follow GA.m order:
%   mu_sbx     N x D     rand for SBX beta
%   sign01     N x D     0/1, used as (-1).^sign01   (GA: randi([0,1],N,D))
%   beta_skip  N x D     GA: beta(rand<0.5)=1
%   proc       N x 1     GA: beta(rand>proC,:)=1
%   site_u     2N x D    GA: Site = rand < proM/D
%   mu_mut     2N x D    polynomial mutation mu
%
% OffspringPreClip is the population AFTER mutation and BEFORE any
% INDIVIDUAL constructor clip. Production GA.m itself does not clip after
% mutation; INDIVIDUAL() does.

    if nargin < 10, proC = 1; end
    if nargin < 11, disC = 15; end
    if nargin < 12, proM = 0.5; end
    if nargin < 13, disM = 20; end

    Parent1 = Parent(1:floor(end/2), :);
    Parent2 = Parent(floor(end/2)+1:floor(end/2)*2, :);
    [N, D] = size(Parent1);

    beta = zeros(N, D);
    mu = mu_sbx;
    beta(mu <= 0.5) = (2 * mu(mu <= 0.5)) .^ (1 / (disC + 1));
    beta(mu > 0.5) = (2 - 2 * mu(mu > 0.5)) .^ (-2 / (disC + 1));
    beta = beta .* ((-1) .^ sign01);
    beta(beta_skip < 0.5) = 1;
    beta(repmat(proc(:) > proC, 1, D)) = 1;
    Offspring = [(Parent1 + Parent2) / 2 + beta .* (Parent1 - Parent2) / 2
                 (Parent1 + Parent2) / 2 - beta .* (Parent1 - Parent2) / 2];

    LowerM = repmat(Lower, 2 * N, 1);
    UpperM = repmat(Upper, 2 * N, 1);
    Site = site_u < proM / D;
    mu2 = mu_mut;
    temp = Site & mu2 <= 0.5;
    Offspring = min(max(Offspring, LowerM), UpperM);
    Offspring(temp) = Offspring(temp) + (UpperM(temp) - LowerM(temp)) .* ...
        ((2 .* mu2(temp) + (1 - 2 .* mu2(temp)) .* ...
        (1 - (Offspring(temp) - LowerM(temp)) ./ (UpperM(temp) - LowerM(temp))) .^ (disM + 1)) .^ (1 / (disM + 1)) - 1);
    temp = Site & mu2 > 0.5;
    Offspring(temp) = Offspring(temp) + (UpperM(temp) - LowerM(temp)) .* ...
        (1 - (2 .* (1 - mu2(temp)) + 2 .* (mu2(temp) - 0.5) .* ...
        (1 - (UpperM(temp) - Offspring(temp)) ./ (UpperM(temp) - LowerM(temp))) .^ (disM + 1)) .^ (1 / (disM + 1)));
    OffspringPreClip = Offspring;
    Offspring = min(max(Offspring, LowerM), UpperM);
end
