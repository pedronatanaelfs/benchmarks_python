function G = ensure_global_mpdmp4(N, evaluation)
%ENSURE_GLOBAL_MPDMP4  Construct the PlatEMO GLOBAL singleton for MPDMP4+OptMPNDS.
    if nargin < 1, N = 200; end
    if nargin < 2, evaluation = 100000; end
    G = GLOBAL('-algorithm', @OptMPNDS, '-problem', @MPDMP4, ...
               '-N', N, '-evaluation', evaluation, '-save', 1);
end
