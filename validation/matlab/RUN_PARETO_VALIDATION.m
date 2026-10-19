%% Targeted MATLAB PS/PF export after objective-equivalence corrections
%
% Open this folder in MATLAB and click Run. This script intentionally skips
% MPMOP4 and MPMOP9 because their supplied true_PS.m attempts a 20000x20000
% mesh and is not safe for normal workstation memory.

clearvars;
clc;

script_dir = fileparts(mfilename('fullpath'));
validation_dir = fileparts(script_dir);
python_repo = fileparts(validation_dir);
project_root = fileparts(python_repo);
zhao_repo = fullfile(project_root, '2026ZhaoNash-main');
opt_repo = fullfile(project_root, 'OptMPNDS-master');
output_dir = fullfile(script_dir, 'pareto_results');
if ~isfolder(output_dir); mkdir(output_dir); end

addpath(fullfile(opt_repo, 'Public'));
addpath(fullfile(zhao_repo, 'MPMOP'), '-begin');
addpath(fullfile(zhao_repo, 'MPDMP'), '-begin');

mpmop_ids = [1:3, 5:8, 10:17];
mpdmp_ids = 1:18;
failures = {};

for id = mpmop_ids
    name = sprintf('MPMOP%d', id);
    try
        global_obj = GLOBAL('-problem', str2func(name), '-D', 10); %#ok<NASGU>
        problem = feval(name);
        PS = problem.PS();
        PF = problem.PF();
        writematrix(PS, fullfile(output_dir, [name '_PS.csv']));
        writematrix(PF, fullfile(output_dir, [name '_PF.csv']));
        fprintf('PASS %s: PS %dx%d, PF %dx%d\n', name, ...
            size(PS,1), size(PS,2), size(PF,1), size(PF,2));
    catch err
        failures(end+1,:) = {name, getReport(err, 'extended', 'hyperlinks', 'off')}; %#ok<SAGROW>
        fprintf(2, 'FAIL %s: %s\n', name, err.message);
    end
end

for id = mpdmp_ids
    name = sprintf('MPDMP%d', id);
    try
        global_obj = GLOBAL('-problem', str2func(name), '-D', 2); %#ok<NASGU>
        problem = feval(name);
        PS = problem.PS();
        PF = problem.PF();
        writematrix(PS, fullfile(output_dir, [name '_PS.csv']));
        writematrix(PF, fullfile(output_dir, [name '_PF.csv']));
        fprintf('PASS %s: PS %dx%d, PF %dx%d\n', name, ...
            size(PS,1), size(PS,2), size(PF,1), size(PF,2));
    catch err
        failures(end+1,:) = {name, getReport(err, 'extended', 'hyperlinks', 'off')}; %#ok<SAGROW>
        fprintf(2, 'FAIL %s: %s\n', name, err.message);
    end
end

fid = fopen(fullfile(output_dir, 'README.txt'), 'w');
fprintf(fid, 'MPMOP4 and MPMOP9 intentionally skipped: unsafe 20000x20000 true_PS mesh.\n');
fprintf(fid, 'Completed problems: %d\n', numel(mpmop_ids)+numel(mpdmp_ids)-size(failures,1));
fprintf(fid, 'Failures: %d\n', size(failures,1));
fclose(fid);

if ~isempty(failures)
    fid = fopen(fullfile(output_dir, 'failures.txt'), 'w');
    for i = 1:size(failures,1)
        fprintf(fid, '===== %s =====\n%s\n\n', failures{i,1}, failures{i,2});
    end
    fclose(fid);
end

fprintf('\nDone. Return folder:\n  %s\n', output_dir);
