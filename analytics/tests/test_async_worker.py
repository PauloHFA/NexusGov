"""
NexusGov - Testes do Disparo Assíncrono e Mensageria (RF-ANA-08 / CA-ANA-08)
"""

import pytest
from analytics.queue.worker import AsyncAnalysisDispatcher, ExecutionStatus


def test_enqueue_analysis_immediate_confirmation():
    """Valida CA-ANA-08: confirmação imediata com ID de execução ao enfileirar."""
    dispatcher = AsyncAnalysisDispatcher()
    task = dispatcher.enqueue_analysis(
        target_orgao_id="PM_CAMPINA_GRANDE",
        versao_parametros="v1.0.0",
        total_items=50
    )

    assert task.task_id is not None
    assert len(task.task_id) == 36
    assert task.status == ExecutionStatus.PENDING
    assert task.progress_pct == 0.0
    assert task.total_contratacoes == 50


def test_task_progress_tracking_and_completion():
    """Valida acompanhamento de progresso e finalização de análise assíncrona."""
    dispatcher = AsyncAnalysisDispatcher()
    task = dispatcher.enqueue_analysis("PM_JOAO_PESSOA", total_items=100)

    # Passo 1: 50% concluído
    updated = dispatcher.process_task_step(task.task_id, items_processed=50)
    assert updated.status == ExecutionStatus.RUNNING
    assert updated.progress_pct == 50.0

    # Passo 2: 100% concluído
    final_task = dispatcher.process_task_step(task.task_id, items_processed=100)
    assert final_task.status == ExecutionStatus.COMPLETED
    assert final_task.progress_pct == 100.0
    assert final_task.completed_at is not None
    assert final_task.resultado is not None


def test_task_failure_handling():
    """Valida tratamento seguro de erros em execução assíncrona."""
    dispatcher = AsyncAnalysisDispatcher()
    task = dispatcher.enqueue_analysis("PM_PATOS", total_items=20)

    failed = dispatcher.fail_task(task.task_id, "Falha de conectividade temporária com a base do PNCP")
    assert failed.status == ExecutionStatus.FAILED
    assert "PNCP" in failed.error_message
