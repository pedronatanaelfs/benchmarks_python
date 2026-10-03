function V = nsidedpoly_vertices(n, center, varargin)
  % Approximate MathWorks nsidedpoly vertex placement.
  % Radius mode: first vertex to the right (angle 0), CCW.
  % SideLength + even n: rotate by pi/n (axis-aligned square).
  radius = [];
  side = [];
  for k = 1:2:numel(varargin)
    key = lower(varargin{k});
    val = varargin{k+1};
    if strcmp(key, 'radius')
      radius = val;
    elseif strcmp(key, 'sidelength')
      side = val;
    end
  end
  if isempty(radius) && isempty(side)
    error('Need Radius or SideLength');
  end
  if ~isempty(side)
    radius = side / (2 * sin(pi / n));
    start = (mod(n, 2) == 0) * (pi / n);
  else
    start = 0;
  end
  ang = start + 2 * pi * (0:n-1) / n;
  V = [center(1) + radius * cos(ang(:)), center(2) + radius * sin(ang(:))];
end
