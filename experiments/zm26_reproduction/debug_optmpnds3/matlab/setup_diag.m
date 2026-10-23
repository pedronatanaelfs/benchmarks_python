function P = setup_diag()
%SETUP_DIAG  OptMPNDS3 diagnostic paths. OptMPNDS3 envsel must win over OptMPNDS.
    thisDir = fileparts(mfilename('fullpath'));
    P.matlabDir = thisDir;
    P.diagRoot = fileparts(thisDir);
    P.shared = fullfile(P.diagRoot, 'shared_inputs');
    P.out = fullfile(P.diagRoot, 'matlab_outputs');
    if exist(P.out, 'dir') ~= 7
        mkdir(P.out);
    end
    P.repoRoot = fileparts(fileparts(fileparts(P.diagRoot)));
    P.she = fullfile(P.repoRoot, 'sources', 'mpdmp_2023', '2022SheOptMPNDS3');
    if exist(P.she, 'dir') ~= 7
        error('She MATLAB source not found: %s', P.she);
    end
    if exist(P.shared, 'dir') ~= 7
        error('shared_inputs/ missing. Run Python diagnostics first.');
    end
    addpath(fullfile(P.she, 'Public'));
    addpath(fullfile(P.she, 'Problems', 'MPDMP'));
    addpath(fullfile(P.she, 'Metrics'));
    addpath(fullfile(P.she, 'Algorithms', 'OptMPNDS'));
    addpath(fullfile(P.she, 'Algorithms', 'OptMPNDS2'));
    addpath(fullfile(P.she, 'Algorithms', 'OptMPNDS3')); % last = first on path
    addpath(thisDir);
end
