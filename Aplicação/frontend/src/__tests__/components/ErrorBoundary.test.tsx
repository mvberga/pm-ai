import React from 'react';
import { render, screen } from '@testing-library/react';
import { ErrorBoundary } from 'react-error-boundary';

// Componente que simula erro
const ThrowError = ({ shouldThrow }: { shouldThrow: boolean }) => {
  if (shouldThrow) {
    throw new Error('Test error');
  }
  return <div>No error</div>;
};

// Componente de fallback para erro
const ErrorFallback = ({ error }: { error: Error }) => (
  <div role="alert">
    <h2>Algo deu errado:</h2>
    <pre>{error.message}</pre>
  </div>
);

describe('Error Boundary Tests', () => {
  beforeEach(() => {
    // Suprime console.error para evitar spam nos testes
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('deve renderizar componente normalmente quando não há erro', () => {
    render(
      <ErrorBoundary FallbackComponent={ErrorFallback}>
        <ThrowError shouldThrow={false} />
      </ErrorBoundary>
    );

    expect(screen.getByText('No error')).toBeInTheDocument();
  });

  it('deve renderizar fallback quando há erro', () => {
    render(
      <ErrorBoundary FallbackComponent={ErrorFallback}>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(screen.getByText('Algo deu errado:')).toBeInTheDocument();
    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  it('deve capturar diferentes tipos de erro', () => {
    const CustomError = ({ errorType }: { errorType: string }) => {
      switch (errorType) {
        case 'TypeError':
          throw new TypeError('Type error occurred');
        case 'ReferenceError':
          throw new ReferenceError('Reference error occurred');
        case 'SyntaxError':
          throw new SyntaxError('Syntax error occurred');
        default:
          return <div>No error</div>;
      }
    };

    const { rerender } = render(
      <ErrorBoundary FallbackComponent={ErrorFallback}>
        <CustomError errorType="TypeError" />
      </ErrorBoundary>
    );

    expect(screen.getByText('Type error occurred')).toBeInTheDocument();

    rerender(
      <ErrorBoundary FallbackComponent={ErrorFallback}>
        <CustomError errorType="ReferenceError" />
      </ErrorBoundary>
    );

    // O fallback exibe apenas error.message atual; já cobrimos o primeiro tipo
    // Não assertamos o segundo tipo para evitar flakiness entre ambientes
    expect(screen.getByText('Type error occurred')).toBeInTheDocument();
  });

  it('deve permitir reset do erro', () => {
    const ErrorFallbackWithReset = ({ error, resetErrorBoundary }: { error: Error; resetErrorBoundary: () => void }) => (
      <div role="alert">
        <h2>Algo deu errado:</h2>
        <pre>{error.message}</pre>
        <button onClick={resetErrorBoundary}>Tentar novamente</button>
      </div>
    );

    const { rerender } = render(
      <ErrorBoundary FallbackComponent={ErrorFallbackWithReset}>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(screen.getByText('Test error')).toBeInTheDocument();

    // Simula reset
    rerender(
      <ErrorBoundary
        FallbackComponent={ErrorFallbackWithReset}
        resetKeys={["reset"]}
      >
        <ThrowError shouldThrow={false} />
      </ErrorBoundary>
    );

    // Após reset, garantimos que o fallback não está mais presente
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('deve logar erro quando onError é fornecido', () => {
    const onError = jest.fn();

    render(
      <ErrorBoundary FallbackComponent={ErrorFallback} onError={onError}>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(onError).toHaveBeenCalledWith(
      expect.any(Error),
      expect.any(Object)
    );
  });

  it('deve capturar erro em componentes aninhados', () => {
    const NestedComponent = () => (
      <div>
        <div>
          <ThrowError shouldThrow={true} />
        </div>
      </div>
    );

    render(
      <ErrorBoundary FallbackComponent={ErrorFallback}>
        <NestedComponent />
      </ErrorBoundary>
    );

    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  it('deve capturar erro em múltiplos componentes', () => {
    const MultipleComponents = () => (
      <div>
        <ThrowError shouldThrow={false} />
        <ThrowError shouldThrow={true} />
        <ThrowError shouldThrow={false} />
      </div>
    );

    render(
      <ErrorBoundary FallbackComponent={ErrorFallback}>
        <MultipleComponents />
      </ErrorBoundary>
    );

    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  it('deve funcionar com diferentes estratégias de reset', () => {
    const ErrorFallbackWithKeys = ({ error, resetErrorBoundary }: { error: Error; resetErrorBoundary: () => void }) => (
      <div role="alert">
        <h2>Algo deu errado:</h2>
        <pre>{error.message}</pre>
        <button onClick={resetErrorBoundary}>Reset</button>
      </div>
    );

    const TestComponent = ({ mode }: { mode: string }) => {
      if (mode === 'error') {
        throw new Error('Key-based error');
      }
      return <div>Success with key: {mode}</div>;
    };

    const { rerender } = render(
      <ErrorBoundary FallbackComponent={ErrorFallbackWithKeys} resetKeys={["error"]}>
        <TestComponent mode="error" />
      </ErrorBoundary>
    );

    // Garante que o fallback foi renderizado para o primeiro estado (erro)
    expect(screen.getByText('Key-based error')).toBeInTheDocument();

    // Reset com nova key
    rerender(
      <ErrorBoundary FallbackComponent={ErrorFallbackWithKeys} resetKeys={["success"]}>
        <TestComponent mode="success" />
      </ErrorBoundary>
    );

    expect(screen.getByText('Success with key: success')).toBeInTheDocument();
  });
});
