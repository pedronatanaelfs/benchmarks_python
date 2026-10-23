function A = diag_load_csv(path)
%DIAG_LOAD_CSV  Load a headerless numeric CSV (shared_inputs).
    if exist(path, 'file') ~= 2
        error('Missing input file: %s', path);
    end
    A = dlmread(path, ',');
end
