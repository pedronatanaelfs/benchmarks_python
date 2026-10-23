function P = setup_diag()
%SETUP_DIAG  Locate diagnostic folders and add original She MATLAB sources.
%
% Path policy: do NOT addpath(genpath(...)) of the whole She tree.
% OptMPNDS / OptMPNDS2 / OptMPNDS3 each ship EnvironmentalSelection.m
% and CrowdingDistance.m; a genpath would make the last folder win.
% This setup puts OptMPNDS first so OptMPNDS diagnostics call the
% original OptMPNDS environmental selection.

    thisDir = fileparts(mfilename('fullpath'));
    P.matlabDir = thisDir;
    P.diagRoot = fileparts(thisDir);
    P.shared = fullfile(P.diagRoot, 'shared_inputs');
    P.out = fullfile(P.diagRoot, 'matlab_outputs');
    if exist(P.out, 'dir') ~= 7
        mkdir(P.out);
    end
    % debug_matlab_python / zm26_reproduction / experiments / benchmarks_python
    P.repoRoot = fileparts(fileparts(fileparts(P.diagRoot)));
    P.she = fullfile(P.repoRoot, 'sources', 'mpdmp_2023', '2022SheOptMPNDS3');
    if exist(P.she, 'dir') ~= 7
        error('She MATLAB source not found: %s', P.she);
    end
    if exist(P.shared, 'dir') ~= 7
        error(['shared_inputs/ is missing. Run Python diagnostics first:\n' ...
               '  python -m experiments.zm26_reproduction.debug_matlab_python.python.run_all_python']);
    end
    addpath(fullfile(P.she, 'Public'));
    addpath(fullfile(P.she, 'Problems', 'MPDMP'));
    addpath(fullfile(P.she, 'Metrics'));
    addpath(fullfile(P.she, 'Algorithms', 'OptMPNDS3'));
    addpath(fullfile(P.she, 'Algorithms', 'OptMPNDS2'));
    addpath(fullfile(P.she, 'Algorithms', 'OptMPNDS')); % last addpath = first on path
    addpath(thisDir);
end
