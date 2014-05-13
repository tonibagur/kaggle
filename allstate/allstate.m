
clear;close all; clc;
more off;
diary on;
fprintf('Loading data...\n');
load allstate.mat;
fprintf('Data loaded!');
fprintf('Adding path to DeepLearnToolbox\n');
addpath(genpath('/home/coneptum/DeepLearnToolbox'));

%The last row of y's is always 0 since in the y's all the vals are allways known
[xtrain,ytrain,xtest,ytest,xval,yval,mu,sigma]=get_train_test_val(X(:,2:size(X,2)),y_a(:,2:size(y_a,2)-1));
save mu_sigma_a.mat mu sigma
select_model(xtrain,ytrain,xtest,ytest,xval,yval,'y_a.mat');


[xtrain,ytrain,xtest,ytest,xval,yval,mu,sigma]=get_train_test_val(X(:,2:size(X,2)),y_b(:,2:size(y_b,2)-1));
save mu_sigma_b.mat mu sigma
select_model(xtrain,ytrain,xtest,ytest,xval,yval,'y_b.mat');

[xtrain,ytrain,xtest,ytest,xval,yval,mu,sigma]=get_train_test_val(X(:,2:size(X,2)),y_c(:,2:size(y_c,2)-1));
save mu_sigma_c.mat mu sigma
select_model(xtrain,ytrain,xtest,ytest,xval,yval,'y_c.mat');


[xtrain,ytrain,xtest,ytest,xval,yval,mu,sigma]=get_train_test_val(X(:,2:size(X,2)),y_d(:,2:size(y_d,2)-1));
save mu_sigma_d.mat mu sigma
select_model(xtrain,ytrain,xtest,ytest,xval,yval,'y_d.mat');

[xtrain,ytrain,xtest,ytest,xval,yval,mu,sigma]=get_train_test_val(X(:,2:size(X,2)),y_e(:,2:size(y_e,2)-1));
save mu_sigma_e.mat mu sigma
select_model(xtrain,ytrain,xtest,ytest,xval,yval,'y_e.mat');


[xtrain,ytrain,xtest,ytest,xval,yval,mu,sigma]=get_train_test_val(X(:,2:size(X,2)),y_f(:,2:size(y_f,2)-1));
save mu_sigma_f.mat mu sigma
select_model(xtrain,ytrain,xtest,ytest,xval,yval,'y_f.mat');


[xtrain,ytrain,xtest,ytest,xval,yval,mu,sigma]=get_train_test_val(X(:,2:size(X,2)),y_g(:,2:size(y_g,2)-1));
save mu_sigma_g.mat mu sigma
select_model(xtrain,ytrain,xtest,ytest,xval,yval,'y_g.mat');
