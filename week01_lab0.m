% COU07506 Week 1, Lab 0 -- Task 1.4 (GNU Octave / MATLAB)
% Run in Octave with: run('week01_lab0.m')
% Only built-in functions are needed; the signal package is not required.
clear; close all; clc;

n = -5:10;
delta = double(n == 0);
step = double(n >= 0);
ramp = n .* step;
expo = (0.8 .^ n) .* step;
sequences = {delta, step, ramp, expo};
titles = {'Unit impulse: delta(n)', 'Unit step: u(n)', ...
          'Unit ramp: n u(n)', 'Exponential: (0.8)^n u(n)'};

figure('Name', 'Task 1.4: Elementary discrete-time sequences', ...
       'Position', [100, 100, 1300, 320]);
for k = 1:4
    subplot(1, 4, k);
    stem(n, sequences{k}, 'filled');
    title(titles{k});
    xlabel('Sample index n (samples)');
    ylabel('Amplitude (dimensionless)');
    grid on;
    xlim([-5, 10]);
end

assert(sum(delta) == 1 && delta(n == 0) == 1);
assert(all(step(n < 0) == 0) && all(step(n >= 0) == 1));
assert(ramp(n == 10) == 10);
assert(abs(expo(n == 1) - 0.8) < 1e-12);
if ~exist('outputs', 'dir')
    mkdir('outputs');
end
print(gcf, fullfile('outputs', 'task_1_4_octave.png'), '-dpng', '-r150');
disp('Task 1.4 complete: four sequences plotted and checked.');
