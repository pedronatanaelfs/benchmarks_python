function A = diag_load_csv(path)
    if exist(path, 'file') ~= 2
        error('Missing input file: %s', path);
    end
    A = dlmread(path, ',');
end
