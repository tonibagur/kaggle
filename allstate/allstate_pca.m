clear;close all; clc;
more off;
diary on;
fprintf('Loading data...\n');
load allstate.mat;
fprintf('Data loaded!\n');
fprintf('Adding path to DeepLearnToolbox\n');
addpath(genpath('/home/coneptum/DeepLearnToolbox'));

fprintf('Doing! pca\n');

X=X(:,2:size(X,2));
[X,mu,sigma]=zscore(X);
size(X);
[U,S]=pca(X);
n=size(S,1);
Srow=zeros(n,1);
for i=1:n
   Srow(i)=S(i,i);
end

cum=zeros(n,1);
for i=1:n
   cum(i)=sum(Srow(1:i))/sum(Srow);
end
cum
K=min(find(cum>=0.99))
Z = projectData(X, U, K);
