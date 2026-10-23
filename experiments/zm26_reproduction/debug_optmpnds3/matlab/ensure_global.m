function G = ensure_global(problemName, N, evaluation)
    if nargin < 2, N = 200; end
    if nargin < 3, evaluation = 100000; end
    switch lower(problemName)
        case 'mpdmp1'
            pb = @MPDMP1;
        case 'mpdmp4'
            pb = @MPDMP4;
        otherwise
            error('Unsupported problem %s', problemName);
    end
    G = GLOBAL('-algorithm', @OptMPNDS3, '-problem', pb, ...
               '-N', N, '-evaluation', evaluation, '-save', 1);
end
